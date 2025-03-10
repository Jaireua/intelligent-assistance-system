# Import libraries
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from .models import UserImages
import face_recognition
import base64

# Create your views here.
def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        face_image_data = request.POST["face_image"]

        # Get the user by username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found."})
        
        # Convert base64 image data to a file
        face_image_data = face_image_data.split(',')[1]
        uploaded_image = ContentFile(base64.b64decode(face_image_data), name=f'{username}.jpg')

        # Compare the uploaded image with the registered image
        uploaded_image = face_recognition.load_image_file(uploaded_image)
        uploaded_face_encoding = face_recognition.face_encodings(uploaded_image)

        if uploaded_face_encoding:
            uploaded_face_encoding = uploaded_face_encoding[0]
            user_image = UserImages.objects.filter(user=user).first()
            stored_face_image = face_recognition.load_image_file(user_image.face_image.path)
            stored_face_encoding = face_recognition.face_encodings(stored_face_image)[0]

            print(stored_face_image, stored_face_encoding)
            # Compare the faces
            match = face_recognition.compare_faces([stored_face_encoding], uploaded_face_encoding)
            if match[0]:
                login(request, user)
                return JsonResponse({"status": "success", "message": "Login successfully.", "redirect": "/admon/"})
            else:
                return JsonResponse({"status": "error", "message": "Face does not match."})

        return JsonResponse({"status": "error", "message": "Face not detected."})

    return render(request, 'home.html')

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
            return JsonResponse({"message": "User registered successfully.", "redirect": "/admon/"})
        except IntegrityError:
            return JsonResponse({"message": "Username already exists."})
        
    return render(request, 'register.html')

@login_required
def signout(request):
    logout(request)
    return redirect('/')

