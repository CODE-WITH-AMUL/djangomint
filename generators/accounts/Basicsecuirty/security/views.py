#-------------------------[IMPORT MODEL]------------------------#
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User



#-------------------------[LOGIN-PAGE]------------------------#

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    return render(request, 'login.html')


#-------------------------[REGISTER-PAGE]------------------------#
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conform_password = request.POST.get('conform_password')
        
        try:
            if password != conform_password:
                messages.error(request, "Passwords do not match.")
                return redirect('register')
            elif username == "" or email == "" or password == "":
                messages.error(request, "All fields are required.")
                return redirect('register')
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    return render(request, 'register.html')


#-------------------------[LOGOUT-PAGE]------------------------#
@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

#-------------------------[HOME-PAGE]------------------------#
@login_required
def home(request):
    return render(request, 'home.html')


