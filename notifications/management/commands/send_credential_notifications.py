from datetime import date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from credentials.models import EmployeeCredential


class Command(BaseCommand):
    help = "Send credential expiration notifications (60, 30, 14 days)."

    def handle(self, *args, **options):
        alert_days = getattr(settings, "CREDENTIAL_ALERT_DAYS", [60, 30, 14])
        admin_recipients = getattr(settings, "CREDENTIAL_ADMIN_RECIPIENTS", [])

        today = date.today()
        alerts = []

        for d in alert_days:
            target_date = today + timedelta(days=d)
            qs = EmployeeCredential.objects.filter(expiration_date=target_date).select_related("employee")
            for cred in qs:
                alerts.append((d, cred))

        if not alerts:
            self.stdout.write("No credential notifications to send today.")
            return

        # ADMIN SUMMARY EMAIL
        if admin_recipients:
            lines = []
            for d, cred in alerts:
                lines.append(
                    f"- {cred.employee} | "
                    f"{cred.get_credential_type_display()} | "
                    f"expires {cred.expiration_date} (in {d} days)"
                )

            send_mail(
                subject="Employee Credential Expiration Alerts",
                message="The following credentials are expiring:\n\n" + "\n".join(lines),
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "alerts@localhost"),
                recipient_list=admin_recipients,
                fail_silently=False,
            )

        # EMPLOYEE EMAILS
        for d, cred in alerts:
            user = cred.employee
            user_email = getattr(user, "email", None)

            if not user_email:
                continue

            message = (
                f"Hello {user.get_full_name() or user.username},\n\n"
                f"This is a reminder that your "
                f"{cred.get_credential_type_display()} "
                f"will expire on {cred.expiration_date} "
                f"(in {d} days).\n\n"
                f"Please upload an updated document or contact the office.\n\n"
                f"Thank you."
            )

            send_mail(
                subject="Your credential is expiring soon",
                message=message,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "alerts@localhost"),
                recipient_list=[user_email],
                fail_silently=False,
            )

        self.stdout.write(self.style.SUCCESS("Credential notifications sent."))
