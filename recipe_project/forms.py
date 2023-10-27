from django import forms

from users.models import CustomUser


class PasswordField(forms.CharField):
    widget = forms.PasswordInput


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = PasswordField(max_length=50)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            raise forms.ValidationError("Please enter a username and password")
        return cleaned_data


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = PasswordField(max_length=50, widget=forms.PasswordInput)
    confirm_password = PasswordField(max_length=50)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def create_user(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user = CustomUser.objects.create_user(username=username, password=password)
        return user
