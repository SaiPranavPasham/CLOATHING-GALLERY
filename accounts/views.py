from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Outfit

# ================= REGISTER =================
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')


# ================= LOGIN =================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


# ================= DASHBOARD =================
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Handle image upload
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            Outfit.objects.create(user=request.user, image=image)
            messages.success(request, "Outfit uploaded successfully")

    # Fetch user images
    images = Outfit.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {'images': images})


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('login')