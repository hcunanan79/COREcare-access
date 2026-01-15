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

### Forgot Your Password?

Contact your administrator to reset your password. They can do this through the Django admin panel.

---

## Troubleshooting

### "Invalid invite code" Error

- Double-check that you entered the invite code exactly as provided (case-sensitive)
- Contact your administrator to verify the current invite code

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
