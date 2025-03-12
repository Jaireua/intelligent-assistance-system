# Import libraries
from django.shortcuts import render

# View signup
def signup(request):
    return render(request, 'signup.html') 