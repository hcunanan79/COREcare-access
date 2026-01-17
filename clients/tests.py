"""
Issue #40: Tests for Client Calendar and Event Management
Includes IDOR security tests (PR blocker), timezone handling, and validation tests.
"""
from datetime import timedelta
from decimal import Decimal

from django.test import TestCase, Client as TestClient
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError

from clients.models import Client, ClientFamilyMember, ClientCalendarEvent
from clients.services import CalendarService
from shifts.models import Shift


class ClientCalendarEventModelTests(TestCase):
    """Test ClientCalendarEvent model validation and methods."""
    
    def setUp(self):
        self.client_obj = Client.objects.create(
            first_name="Test",
            last_name="Client"
        )
        self.user = User.objects.create_user(
            username="familyuser",
            password="testpass123"
        )
    
    def test_create_valid_event(self):
        """Test creating a valid calendar event."""
        event = ClientCalendarEvent.objects.create(
            client=self.client_obj,
            title="Doctor Appointment",
            event_type="medical",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            location="Dr. Smith's Office",
            created_by=self.user
        )
        self.assertIsNotNone(event.id)
        self.assertEqual(event.title, "Doctor Appointment")
        self.assertEqual(event.event_type, "medical")
        self.assertFalse(event.is_deleted)
    
    def test_end_time_before_start_time_raises_error(self):
        """Test that end_time before start_time raises ValidationError."""
        with self.assertRaises(ValidationError) as context:
            ClientCalendarEvent.objects.create(
                client=self.client_obj,
                title="Invalid Event",
                event_type="other",
                start_time=timezone.now() + timedelta(hours=1),
                end_time=timezone.now(),  # Before start_time
                created_by=self.user
            )
        self.assertIn('end_time', str(context.exception))
    
    def test_end_time_equals_start_time_raises_error(self):
        """Test that end_time equal to start_time raises ValidationError."""
        now = timezone.now()
        with self.assertRaises(ValidationError):
            ClientCalendarEvent.objects.create(
                client=self.client_obj,
                title="Zero Duration Event",
                event_type="other",
                start_time=now,
                end_time=now,  # Same as start_time
                created_by=self.user
            )
    
    def test_soft_delete(self):
        """Test soft delete functionality."""
        event = ClientCalendarEvent.objects.create(
            client=self.client_obj,
            title="To Be Deleted",
            event_type="social",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            created_by=self.user
        )
        event_id = event.id
        
        # Soft delete
        event.soft_delete()
        
        # Should not appear in default queryset
        self.assertEqual(ClientCalendarEvent.objects.filter(id=event_id).count(), 0)
        
        # Should appear in all_objects
        self.assertEqual(ClientCalendarEvent.all_objects.filter(id=event_id).count(), 1)
        
        # Verify is_deleted property
        event.refresh_from_db()
        self.assertTrue(event.is_deleted)
    
    def test_restore_soft_deleted_event(self):
        """Test restoring a soft-deleted event."""
        event = ClientCalendarEvent.objects.create(
            client=self.client_obj,
            title="To Be Restored",
            event_type="family",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            created_by=self.user
        )
        event.soft_delete()
        event.restore()
        
        self.assertFalse(event.is_deleted)
        self.assertEqual(ClientCalendarEvent.objects.filter(id=event.id).count(), 1)
    
    def test_event_type_icon(self):
        """Test event type icon property."""
        event = ClientCalendarEvent(event_type="medical")
        self.assertEqual(event.event_type_icon, "🩺")
        
        event.event_type = "social"
        self.assertEqual(event.event_type_icon, "👥")
        
        event.event_type = "therapy"
        self.assertEqual(event.event_type_icon, "💆")


class CalendarServiceTests(TestCase):
    """Test CalendarService functionality."""
    
    def setUp(self):
        self.client_obj = Client.objects.create(
            first_name="Test",
            last_name="Client"
        )
        self.caregiver = User.objects.create_user(
            username="caregiver",
            password="testpass123",
            first_name="Jane",
            last_name="Caregiver"
        )
        self.family_user = User.objects.create_user(
            username="familymember",
            password="testpass123",
            first_name="John",
            last_name="Family"
        )
        
        # Create a shift
        self.shift = Shift.objects.create(
            client=self.client_obj,
            caregiver=self.caregiver,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=8),
            pay_rate=Decimal("25.00"),
            bill_rate=Decimal("35.00")
        )
        
        # Create an event
        self.event = ClientCalendarEvent.objects.create(
            client=self.client_obj,
            title="Doctor Appointment",
            event_type="medical",
            start_time=timezone.now() + timedelta(days=2),
            end_time=timezone.now() + timedelta(days=2, hours=1),
            location="Dr. Smith",
            created_by=self.family_user
        )
    
    def test_get_client_schedule_includes_both_shifts_and_events(self):
        """Test that schedule includes both shifts and events."""
        schedule = CalendarService.get_client_schedule(self.client_obj.id)
        
        self.assertEqual(len(schedule), 2)
        types = [item['type'] for item in schedule]
        self.assertIn('shift', types)
        self.assertIn('event', types)
    
    def test_get_client_schedule_sorted_by_start_time(self):
        """Test that schedule is sorted by start_time."""
        schedule = CalendarService.get_client_schedule(self.client_obj.id)
        
        for i in range(len(schedule) - 1):
            self.assertLessEqual(schedule[i]['start_time'], schedule[i + 1]['start_time'])
    
    def test_get_client_schedule_excludes_soft_deleted_events(self):
        """Test that soft-deleted events are excluded."""
        self.event.soft_delete()
        
        schedule = CalendarService.get_client_schedule(self.client_obj.id)
        
        event_ids = [item['id'] for item in schedule if item['type'] == 'event']
        self.assertNotIn(self.event.id, event_ids)
    
    def test_get_client_schedule_respects_date_range(self):
        """Test that schedule respects date range filters."""
        # Create an event outside the range
        far_future_event = ClientCalendarEvent.objects.create(
            client=self.client_obj,
            title="Far Future Event",
            event_type="other",
            start_time=timezone.now() + timedelta(days=100),
            end_time=timezone.now() + timedelta(days=100, hours=1),
            created_by=self.family_user
        )
        
        # Query for next 7 days only
        schedule = CalendarService.get_client_schedule(
            self.client_obj.id,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=7)
        )
        
        event_ids = [item['id'] for item in schedule if item['type'] == 'event']
        self.assertNotIn(far_future_event.id, event_ids)


class IDORSecurityTests(TestCase):
    """
    IDOR (Insecure Direct Object Reference) security tests.
    These are PR blockers per the engineering committee decision.
    """
    
    def setUp(self):
        # Create two separate clients
        self.client_a = Client.objects.create(
            first_name="Client",
            last_name="A"
        )
        self.client_b = Client.objects.create(
            first_name="Client",
            last_name="B"
        )
        
        # Create users
        self.user_a = User.objects.create_user(
            username="user_a",
            password="testpass123"
        )
        self.user_b = User.objects.create_user(
            username="user_b",
            password="testpass123"
        )
        
        # Link user_a to client_a only
        ClientFamilyMember.objects.create(
            client=self.client_a,
            user=self.user_a,
            relationship="Son",
            can_view_schedule=True
        )
        
        # Link user_b to client_b only
        ClientFamilyMember.objects.create(
            client=self.client_b,
            user=self.user_b,
            relationship="Daughter",
            can_view_schedule=True
        )
        
        # Create an event for client_b
        self.event_b = ClientCalendarEvent.objects.create(
            client=self.client_b,
            title="Client B Event",
            event_type="medical",
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1),
            created_by=self.user_b
        )
        
        self.test_client = TestClient()
    
    def test_user_cannot_view_unlinked_client_calendar(self):
        """User A cannot view Client B's calendar."""
        self.test_client.login(username="user_a", password="testpass123")
        
        response = self.test_client.get(
            reverse('client_calendar', kwargs={'client_id': self.client_b.id})
        )
        
        # Should get 403 Forbidden
        self.assertEqual(response.status_code, 403)
    
    def test_user_cannot_create_event_for_unlinked_client(self):
        """User A cannot create an event for Client B."""
        self.test_client.login(username="user_a", password="testpass123")
        
        response = self.test_client.post(
            reverse('create_event', kwargs={'client_id': self.client_b.id}),
            {
                'title': 'Malicious Event',
                'event_type': 'other',
                'start_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'start_time': '09:00',
                'end_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'end_time': '10:00',
            }
        )
        
        # Should get 403 Forbidden
        self.assertEqual(response.status_code, 403)
        
        # Verify no event was created
        self.assertEqual(
            ClientCalendarEvent.objects.filter(client=self.client_b, title='Malicious Event').count(),
            0
        )
    
    def test_user_cannot_edit_event_for_unlinked_client(self):
        """User A cannot edit an event for Client B."""
        self.test_client.login(username="user_a", password="testpass123")
        
        response = self.test_client.post(
            reverse('edit_event', kwargs={
                'client_id': self.client_b.id,
                'event_id': self.event_b.id
            }),
            {
                'title': 'Hacked Event',
                'event_type': 'other',
                'start_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'start_time': '09:00',
                'end_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'end_time': '10:00',
            }
        )
        
        # Should get 403 Forbidden
        self.assertEqual(response.status_code, 403)
        
        # Verify event was not modified
        self.event_b.refresh_from_db()
        self.assertEqual(self.event_b.title, 'Client B Event')
    
    def test_user_cannot_delete_event_for_unlinked_client(self):
        """User A cannot delete an event for Client B."""
        self.test_client.login(username="user_a", password="testpass123")
        
        response = self.test_client.post(
            reverse('delete_event', kwargs={
                'client_id': self.client_b.id,
                'event_id': self.event_b.id
            })
        )
        
        # Should get 403 Forbidden
        self.assertEqual(response.status_code, 403)
        
        # Verify event still exists
        self.assertTrue(
            ClientCalendarEvent.all_objects.filter(id=self.event_b.id, deleted_at__isnull=True).exists()
        )
    
    def test_user_cannot_access_calendar_api_for_unlinked_client(self):
        """User A cannot access the calendar API for Client B."""
        self.test_client.login(username="user_a", password="testpass123")
        
        response = self.test_client.get(
            reverse('calendar_api', kwargs={'client_id': self.client_b.id})
        )
        
        # Should get 403 Forbidden
        self.assertEqual(response.status_code, 403)
    
    def test_linked_user_can_view_calendar(self):
        """User A CAN view Client A's calendar (positive test)."""
        self.test_client.login(username="user_a", password="testpass123")
        
        response = self.test_client.get(
            reverse('client_calendar', kwargs={'client_id': self.client_a.id})
        )
        
        # Should succeed
        self.assertEqual(response.status_code, 200)
    
    def test_linked_user_can_create_event(self):
        """User A CAN create an event for Client A (positive test)."""
        self.test_client.login(username="user_a", password="testpass123")
        
        response = self.test_client.post(
            reverse('create_event', kwargs={'client_id': self.client_a.id}),
            {
                'title': 'Valid Event',
                'event_type': 'medical',
                'start_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'start_time': '09:00',
                'end_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'end_time': '10:00',
            }
        )
        
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        
        # Verify event was created
        self.assertEqual(
            ClientCalendarEvent.objects.filter(client=self.client_a, title='Valid Event').count(),
            1
        )


class PermissionFlagTests(TestCase):
    """Test that can_view_schedule permission is respected."""
    
    def setUp(self):
        self.client_obj = Client.objects.create(
            first_name="Test",
            last_name="Client"
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.test_client = TestClient()
    
    def test_user_without_schedule_permission_cannot_view_calendar(self):
        """User with can_view_schedule=False cannot view calendar."""
        ClientFamilyMember.objects.create(
            client=self.client_obj,
            user=self.user,
            can_view_schedule=False  # No schedule permission
        )
        
        self.test_client.login(username="testuser", password="testpass123")
        
        response = self.test_client.get(
            reverse('client_calendar', kwargs={'client_id': self.client_obj.id})
        )
        
        # Should get 403 Forbidden
        self.assertEqual(response.status_code, 403)
