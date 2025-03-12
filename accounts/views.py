# Import libraries
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# View signup
@csrf_exempt
def signup(request):
    return render(request, 'signup.html') 