# Import libraries
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import base64
from django.http import JsonResponse
from .models import UserImages

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('/')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm, "error": "Username already exists."})
        else:
            return render(request, 'signup.html', {'form': UserCreationForm, "error": "Passwords do not match."})

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate (request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, "error": "Invalid credentials."})
        else:
            login(request, user)
            return redirect('/admon/')

@login_required
def admon(request):
    return render(request, 'admon.html')

@login_required
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        face_image_data = request.POST['face_image']

        # Convert base64 image date to a file
        face_image_data = face_image_data.split(',')[1]
        face_image = ContentFile(base64.b64decode(face_image_data), name=f'{username}.jpg')

        # Save the user and face image in the database
        try:
            user = User(username=username)
            user.save()
            user_image = UserImages.objects.create(user=user, face_image=face_image)
            return JsonResponse({"message": "User registered successfully."})
        except IntegrityError:
            return JsonResponse({"message": "Username already exists."})
        
    return render(request, 'register.html')


