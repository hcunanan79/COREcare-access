from django import forms
from django.contrib.auth.models import User
from django.conf import settings


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password"}),
    )
    invite_code = forms.CharField(
        label="Invite Code",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter invite code"}),
        help_text="Enter the invite code provided by your administrator.",
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
        }

    def clean_invite_code(self):
        """Validate the invite code against the configured code."""
        invite_code = self.cleaned_data.get("invite_code")
        valid_code = getattr(settings, "EMPLOYEE_INVITE_CODE", None)

        if not valid_code:
            raise forms.ValidationError("Employee registration is currently disabled.")

        if invite_code != valid_code:
            raise forms.ValidationError("Invalid invite code. Please contact your administrator.")

        return invite_code

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
