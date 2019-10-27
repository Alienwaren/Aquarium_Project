from pathlib import Path
from typing import Dict

from monitor.tools import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from aquarium_django.text.template import TextTemplate
from aquarium_django.text.evaluator import MarkdownTextEvaluator
from monitor.forms import RegisterForm, LoginForm, AddNewPetForm, AddNewHabitatForm
import bcrypt
from monitor.models import User, Pet, Habitat, ApiKey
from aquarium_django.helpers import api_key


def index(request) -> HttpResponse:
    template_parser = TextTemplate(MarkdownTextEvaluator)
    templates = template_parser.templates_from_files([Path("static/markdown/index/get_started.md"),
                                                      Path("static/markdown/index/pricing.md"),
                                                      Path("static/markdown/index/documentation.md")], [{}, {}, {}])
    return render(request, "index/index.html", templates)


def about(request) -> HttpResponse:
    template = TextTemplate(MarkdownTextEvaluator)
    rendered_template = template.template_from_file(Path("static/markdown/about_content.md"), {})
    return render(request, "index/about.html", {"markdown_content": rendered_template})


def register(request) -> HttpResponse:
    msg = "Fill out following form to create new user account."
    register_form = RegisterForm()
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            if register_form.data['password'] == register_form.data['password_repeated']:
                password_hash = bcrypt.hashpw(register_form.data['password'].encode(), bcrypt.gensalt(17))
                new_user = User()
                new_user.email = register_form.data['email']
                new_user.username = register_form.data['username']
                new_user.password = password_hash.decode()
                new_user.save()
                msg = "Registration succeeded. You may now login."
        else:
            msg = "Invalid data supplied. Check registration form and try again."
    return render(request, "index/register.html", {"register_form": register_form, "form_msg": msg})


def login(request) -> HttpResponse:
    if request.session.get('logged_in', False) and request.session.get('username', ""):
        return redirect('user_page')

    msg = "Username and password fields are case sensitive"
    login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            users = User.objects.filter(username=login_form.data['username'])
            if not users:
                msg = "User does not exist. Please register."
            else:
                fetched_username = users[0].username
                fetched_password_hash = users[0].password
                if fetched_username == login_form.data['username']:
                    if bcrypt.checkpw(login_form.data['password'].encode(), fetched_password_hash.encode()):
                        request.session['logged_in'] = True
                        request.session['username'] = login_form.data['username']
                        return redirect("user_page")
                    else:
                        msg = "Incorrect password."
                else:
                    msg = "Incorrect username."

    return render(request, "index/login.html", {"login_form": login_form, "form_msg": msg})


@login_required
def user_page(request) -> HttpResponse:
    user = User.objects.filter(username=request.session['username'])[0]
    habitats = Habitat.objects.select_related("inhabitant").all()
    owned_habitats = [habitat for habitat in habitats if habitat.inhabitant.owner.username == user.username]
    return render(request, "user/user_page.html", {
        "logged_in": request.session['logged_in'],
        "username": request.session['username'],
        "habitats": owned_habitats,
    })


@login_required
def logout(request) -> HttpResponse:
    del request.session['logged_in']
    request.session['username'] = ""
    return redirect("login")


@login_required
def add_new_pet(request) -> HttpResponse:
    msg = f"Fill all nessesary fields."
    add_new_pet_form = AddNewPetForm()
    if request.method == "POST":
        add_new_pet_form = AddNewPetForm(request.POST)
        if add_new_pet_form.is_valid():
            pet = Pet(pet_name=add_new_pet_form.data['pet_name'], pet_type=add_new_pet_form.data['pet_type'],
                      pet_species=add_new_pet_form.data['pet_species'])
            user = User.objects.filter(username=request.session['username']).first()
            pet.owner = user
            pet.save()
            msg = f"Pet added successfully."
        else:
            msg = "Please correct the form."

    return render(request, "user/add_new_pet.html", {"add_pet_form": add_new_pet_form, "msg": msg,
                                                     "logged_in": request.session['logged_in']})


@login_required
def add_new_habitat(request):
    msg = f"Fill all nessesary fields."
    add_habitat_form = AddNewHabitatForm()
    user = User.objects.filter(username=request.session['username']).first()
    pets = Pet.objects.filter(owner=user)
    add_habitat_form.fields['pet'].queryset = pets
    if request.method == "POST":
        add_habitat_form = AddNewHabitatForm(request.POST)
        add_habitat_form.fields['pet'].queryset = pets
        if add_habitat_form.is_valid():
            inhabitant = Pet.objects.filter(id=add_habitat_form.data['pet'])[0]
            habitat_type = add_habitat_form.data['habitat_type']
            new_habitat = Habitat(inhabitant=inhabitant, habitat_type=habitat_type, actual_temperature=0,

                                  actual_insolation=0)
            new_habitat.save()
            msg = f"Habitat saved, you can now add sensors to habitat."

    return render(request, "user/add_new_habitat.html", {"add_habitat_form": add_habitat_form, "msg": msg,
                                                         "logged_in": request.session['logged_in'], })


@login_required
def habitat_page(request, params: Dict):
    user = User.objects.filter(username=request.session['username']).first()
    pet = Pet.objects.filter(owner=user, pet_name=params['pet']).first()
    habitat = Habitat.objects.filter(inhabitant=pet).first()
    habitat_api_key = ApiKey.objects.filter(habitat_owner=habitat).first()
    actual_temperature = habitat.actual_temperature
    actual_insolation = habitat.actual_insolation
    msg = f"{params['pet']}'s Habitat"
    return render(request, "user/habitat_page.html", {"msg": msg,
                                                      "logged_in": request.session['logged_in'], "pet": params['pet'],
                                                      "temperature": actual_temperature,
                                                      "insolation": actual_insolation,
                                                      "api_key": habitat_api_key.api_key})


@login_required
def manage_habitat(request, params: Dict):
    user = User.objects.filter(username=request.session['username']).first()
    pet = Pet.objects.filter(owner=user, pet_name=params['pet']).first()
    habitat = Habitat.objects.filter(inhabitant=pet).first()
    habitat_key = ApiKey.objects.filter(habitat_owner=habitat).first()
    if habitat_key is None:
        key = api_key.generate(17)  # dont ask my why 17
        api_key_object = ApiKey()
        api_key_object.api_key = key
        api_key_object.habitat_owner = habitat
        api_key_object.save()
    msg = f"Manage {params['pet']}'s habitat"
    return render(request, "user/manage_habitat.html", {"msg": msg,
                                                        "logged_in": request.session['logged_in'],
                                                        "api_key": habitat_key.api_key})
