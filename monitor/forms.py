from django import forms

from monitor.models import Pet


class RegisterForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(label="Username", max_length=50, min_length=1)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), min_length=6)
    password_repeated = forms.CharField(label="Repeat password", widget=forms.PasswordInput(), min_length=6)


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), min_length=6)


class AddNewPetForm(forms.Form):
    pet_name = forms.CharField(label="Pet name", max_length=50)
    pet_type = forms.CharField(label="Pet type", max_length=75)
    pet_species = forms.CharField(label="Pet species", max_length=150)


class AddNewHabitatForm(forms.Form):
    pet = forms.ModelChoiceField(queryset=Pet.objects.none())
    habitat_type = forms.CharField(max_length=150)
