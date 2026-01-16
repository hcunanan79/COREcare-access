# Security & Compliance Architecture

COREcare Access is designed with HIPAA-compliant principles to ensure data integrity and patient privacy.

## 1. Authentication & Access Control

### 1.1 Strict Session Management
- **Framework**: Django Authentication System (PBKDF2 password hashing).
- **Session Security**: 
  - `SESSION_COOKIE_SECURE = True` (Production)
  - `CSRF_COOKIE_SECURE = True`
  - HttpOnly cookies to prevent XSS theft.
- **Registration Gates**: New accounts require a periodic `EMPLOYEE_INVITE_CODE`.

### 1.2 Row-Level Security
- **Caregiver Isolation**: Caregivers can ONLY view shifts assigned to their `user_id`. Attempting to view another caregiver's shift returns 403/404.
- **Family Isolation**: Family members can ONLY view clients explicitly linked via `ClientFamilyMember` table.

## 2. Audit & Accountability (Phase 3)

### 2.1 Immutable Clock Logs (`ClockEvent`)
- **Purpose**: Dispute resolution and fraud prevention.
- **Data Captured**:
  - Exact Server Timestamp (cannot be spoofed by client).
  - GPS Coordinates (`latitude`, `longitude`).
  - IP Address and User Agent.
  - Event Type (CLOCK_IN / CLOCK_OUT).
- **Integrity**: Records are created mostly-read-only. Admin interface for these is restricted.

### 2.2 Shift Verification
- **Geolocation**: Browser Geolocation API is required for all clock actions. Coordinates are stored permanently with the Visit.
- **Mileage Cap**: Hard limit of 500 miles per visit to prevent data entry errors or fraud.

## 3. Rate Limiting (Phase 2)

To prevent brute-force attacks and DDOS:
- **Login**: Max 5 attempts per IP per minute.
- **Clock-In**: Max 10 attempts per user per minute (prevents double-tap errors).
- **API**: General throttle on all `/api/` endpoints.
**(Note: Implementation relies on `django-ratelimit` or web server config).**

## 4. Workflows for Compliance

### 4.1 Dispute Resolution
If a caregiver claims the app failed:
1. Admin checks `ClockEvent` table.
2. Checks for "Offline Sync" flags.
3. Compares Server Timestamp vs. Claimed Time.

### 4.2 Offline Data Protection (PWA)
- Data stored in browser `localStorage` is transient.
- No sensitive PHI (Patient Health Info) is cached persistently on the device beyond the active session requirements.
- Sync mechanism moves data to secure server ASAP.

## 5. Future Roadmap
- **2FA**: Two-factor authentication for Admin accounts.
- **Audit Export**: Automated CSV export for payroll auditing.
