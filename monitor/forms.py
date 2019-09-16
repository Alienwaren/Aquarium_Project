from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(label="Username", max_length=50, min_length=1)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), min_length=6)
    password_repeated = forms.CharField(label="Repeat password", widget=forms.PasswordInput(), min_length=6)


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), min_length=6)
