# Employee Onboarding Guide

This guide explains how to invite and onboard new employees to COREcare Access.

## For Administrators

### Inviting New Employees

1. **Share the signup URL** with the new employee:
   ```
   https://corecare-access.onrender.com/portal/signup/
   ```

2. **Provide the invite code**: `CORECARE`

   > The invite code is required to create an account. Without it, registration will fail.

3. **Employee completes registration** by filling out:
   - Username
   - Email address
   - Password (and confirmation)
   - Invite code

4. **After signup**, the employee is automatically logged in and redirected to their dashboard.

### Changing the Invite Code

To change the invite code (recommended periodically for security):

1. Go to your [Render Dashboard](https://dashboard.render.com)
2. Select the **COREcare-access** service
3. Navigate to **Environment** settings
4. Update the `EMPLOYEE_INVITE_CODE` variable
5. The service will automatically redeploy with the new code

### Disabling Employee Registration

To temporarily disable self-registration:

1. Remove the `EMPLOYEE_INVITE_CODE` environment variable from Render
2. Employees will see "Employee registration is currently disabled" when attempting to sign up

---

## For New Employees

### Creating Your Account

1. **Navigate to the signup page**:
   ```
   https://corecare-access.onrender.com/portal/signup/
   ```

2. **Fill out the registration form**:
   - **Username**: Choose a unique username (this is what you'll use to log in)
   - **Email**: Your email address
   - **Password**: Create a secure password
   - **Confirm Password**: Re-enter your password
   - **Invite Code**: Enter the code provided by your administrator

3. **Click "Sign Up"** to create your account

4. You'll be automatically logged in and taken to your dashboard

### Logging In (Returning Users)

1. **Navigate to the login page**:
   ```
   https://corecare-access.onrender.com/portal/login/
   ```

2. **Enter your credentials**:
   - Username
   - Password

3. **Click "Log In"** to access your dashboard

### 📱 Install the App (Recommended)

COREcare Access works offline! To get the best experience:

**On iPhone (Safari):**
1. Tap the **Share** button (box with arrow).
2. Scroll down and tap **"Add to Home Screen"**.
3. Takes you to your home screen like a native app.

**On Android (Chrome):**
1. Tap the menu (three dots).
2. Tap **"Install App"** or "Add to Home Screen".
3. The app is now installed on your phone.

---

## Daily Usage Requirements

### 📍 Location Services
You **MUST allow location access** to clock in and out. The app uses GPS to verify you are at the client's home.
- If denied, you will see an error message.
- Go to your Phone Settings -> Privacy -> Location Services to enable it for your browser.

### 🚗 Mileage Reporting
- You must enter mileage when clocking out.
- The system checks for realistic values (Max 500 miles allowed per visit).

### 📶 Offline Mode
- If you lose signal, **keep working!**
- Clock In/Out even without internet.
- The app will say "Offline Mode Active" (Orange banner).
- When you get back to signal, the app will automatically sync your times.

### Forgot Your Password?

Contact your administrator to reset your password. They can do this through the Django admin panel.

---

## Troubleshooting

### "Invalid invite code" Error

- Double-check that you entered the invite code exactly as provided (case-sensitive)
- Contact your administrator to verify the current invite code

### "Location Access Denied" Error

- You clicked "Block" when asked for location.
- Reset permission in your browser settings (click the lock icon in URL bar).

### "Employee registration is currently disabled" Error

- Self-registration has been temporarily disabled
- Contact your administrator to have them create an account for you manually

### "Username already exists" Error

- The username you chose is already taken
- Try a different username (e.g., add numbers or use your full name)

### Can't Log In After Registration

- Verify you're using the correct username (not your email)
- Check that Caps Lock is off
- Try resetting your password through your administrator

---

## Security Best Practices

### For Administrators

- Change the invite code periodically (monthly recommended)
- Use a non-obvious invite code in production
- Disable registration when not actively onboarding employees
- Review the user list regularly in the admin panel

### For Employees

- Use a strong, unique password
- Don't share your login credentials
- Log out when using shared computers
- Report any suspicious activity to your administrator

---

## Related Links

- [Admin Panel](https://corecare-access.onrender.com/admin/) - For administrators
- [Employee Login](https://corecare-access.onrender.com/portal/login/) - For returning users
- [Employee Signup](https://corecare-access.onrender.com/portal/signup/) - For new employees
