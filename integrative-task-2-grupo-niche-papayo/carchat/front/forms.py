from django import forms
from .models import Usuario

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="confirm_password")

    class Meta:
        model = Usuario
        fields = ['name', 'lastName', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("No match in Passwords.")
        return cleaned_data

class UserLoginForm(forms.Form):
    email = forms.EmailField(label="email")
    password = forms.CharField(widget=forms.PasswordInput, label="password")