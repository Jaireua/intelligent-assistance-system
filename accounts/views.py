from django.shortcuts import render
import face_recognition
import base64
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.base import ContentFile
from .models import UserImage, User
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        face_image_data = request.POST['face_image']

        # Convert base64 image data to a file
        face_image_data = face_image_data.split(',')[1] # Remove the "data:image/jpeg;base64,"
        face_image = ContentFile(base64.b64decode(face_image_data), name=f'{username}.jpg')

        # Save the user and face image to the database
        user = User(username=username)
        user.save()
        user_image = UserImage.objects.create(user=user, face_image=face_image)
        
        # Return a success message
        return JsonResponse({'status': 'success', 'message': 'Registered successfully!'})

    return render(request, 'register.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        face_image_data = request.POST['face_image']

         # Get the user by username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'})
        
        # Convert base64 image data to a file
        face_image_data = face_image_data.split(',')[1] # Remove the "data:image/jpeg;base64,"
        uploaded_image = ContentFile(base64.b64decode(face_image_data), name=f'{username}.jpg')

        # Compare the uploaded face image with the stored face image
        uploaded_face_image = face_recognition.load_image_file(uploaded_image)
        uploaded_face_encoding = face_recognition.face_encodings(uploaded_face_image)

        if uploaded_face_encoding:
            uploaded_face_encoding = uploaded_face_encoding[0]
            user_image = UserImage.objects.filter(user=user).first()
            stored_face_image = face_recognition.load_image_file(user_image.face_image.path)
            stored_face_encoding = face_recognition.face_encodings(stored_face_image[0])

            print(stored_face_image, stored_face_encoding)
            # Compare the face encodings
            match = face_recognition.compare_faces([stored_face_encoding], uploaded_face_encoding)
            if match[0]:
                return JsonResponse({'status': 'success', 'message': 'Login successful!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Face recognition failed.'})
        
        return JsonResponse({'status': 'error', 'message': 'No face detected in the image.'})
    
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')