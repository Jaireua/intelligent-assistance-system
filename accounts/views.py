from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm # import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import IntegrityError

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
                return HttpResponse("User created successfully.")
                #login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm, "error": "Username already exists."})
        return  HttpResponse("Passwords do not match.")
        #return render(request, 'signup.html', {'form': UserCreationForm, "error": "Passwords do not match."})

    

    