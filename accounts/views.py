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
def register(request):
    """
    View for user registration with facial recognition.
    
    This function handles both the presentation of the registration form (GET request)
    and the processing of submitted data (POST request). It captures a facial image
    and creates a new user account with associated facial data.
    
    Args:
        request: Django HttpRequest object containing user data and facial image
        
    Returns:
        HttpResponse: Renders the registration template or returns a JSON response
    """
    if request.method == 'POST':
        username = request.POST['username']
        face_image_data = request.POST['face_image']

        # Check if the user already exists in the database
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Username already exists. Please choose another one.'
            })

        # Convert base64 image data to a file object
        face_image_data = face_image_data.split(',')[1]  # Remove "data:image/jpeg;base64," prefix
        face_image = ContentFile(base64.b64decode(face_image_data), name=f'{username}.jpg')

        try:
            # Save the user and face image to the database
            user = User(username=username)
            user.save()
            user_image = UserImage.objects.create(user=user, face_image=face_image)
            
            return JsonResponse({'status': 'success', 'message': 'Registered successfully!'})
        except Exception as e:
            # Handle any exceptions during registration
            return JsonResponse({
                'status': 'error',
                'message': f'Error registering user: {str(e)}'
            })

    # If it's a GET request, show the registration form
    return render(request, 'register.html')

@csrf_exempt
def login(request):
    """
    View for user login with facial recognition.
    
    This function handles both the presentation of the login form (GET request)
    and the processing of submitted data (POST request). It verifies the user's
    identity by comparing the captured facial image with the stored facial data.
    
    Args:
        request: Django HttpRequest object containing username and facial image
        
    Returns:
        HttpResponse: Renders the login template or returns a JSON response
    """
    if request.method == 'POST':
        username = request.POST['username']
        face_image_data = request.POST['face_image']

        # Check if the user exists in the database
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User does not exist.'})

        # Convert base64 image data to a file object
        face_image_data = face_image_data.split(',')[1]  # Remove "data:image/jpeg;base64," prefix
        uploaded_image = ContentFile(base64.b64decode(face_image_data), name=f'{username}.jpg')

        # Process facial recognition
        uploaded_face_image = face_recognition.load_image_file(uploaded_image)
        uploaded_face_encoding = face_recognition.face_encodings(uploaded_face_image)

        if uploaded_face_encoding:
            # If a face is detected in the uploaded image
            uploaded_face_encoding = uploaded_face_encoding[0]
            user_image = UserImage.objects.filter(user=user).first()
            
            if not user_image:
                return JsonResponse({'status': 'error', 'message': 'No facial image registered for this user.'})
                
            # Load the stored facial image for comparison
            stored_face_image = face_recognition.load_image_file(user_image.face_image.path)
            stored_face_encoding = face_recognition.face_encodings(stored_face_image)
            
            if not stored_face_encoding:
                return JsonResponse({'status': 'error', 'message': 'Could not detect a face in the stored image.'})
                
            stored_face_encoding = stored_face_encoding[0]

            # Compare the face encodings
            match = face_recognition.compare_faces([stored_face_encoding], uploaded_face_encoding)
            if match[0]:
                return JsonResponse({'status': 'success', 'message': 'Login successful!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Face recognition failed.'})
        
        return JsonResponse({'status': 'error', 'message': 'No face detected in the image.'})
    
    # If it's a GET request, show the login form
    return render(request, 'login.html')

def home(request):
    """
    View for the home page of the application.
    
    This is a simple view that renders the home page template.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        HttpResponse: Renders the home page template
    """
    return render(request, 'home.html')