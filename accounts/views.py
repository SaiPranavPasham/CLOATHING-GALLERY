from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import Outfit, WishlistItem


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not username or not email or not password:
            error = 'All fields are required'
            messages.error(request, error)
            return render(request, 'register.html', {'error': error})

        if User.objects.filter(username=username).exists():
            error = 'Username already exists'
            messages.error(request, error)
            return render(request, 'register.html', {'error': error})

        if User.objects.filter(email=email).exists():
            error = 'Email already exists'
            messages.error(request, error)
            return render(request, 'register.html', {'error': error})

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully')
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('dashboard')

        error = 'Invalid credentials'
        messages.error(request, error)
        return render(request, 'login.html', {'error': error})

    return render(request, 'login.html')


@login_required
def dashboard_view(request):
    outfits = request.user.outfits.all()
    context = {
        'outfits': outfits,
        'outfit_count': outfits.count(),
    }
    return render(request, 'dashboard.html', context)


@login_required
def favorites_view(request):
    outfits = request.user.outfits.filter(is_favorite=True)
    context = {
        'outfits': outfits,
        'outfit_count': outfits.count(),
    }
    return render(request, 'favorites.html', context)


@login_required
def wishlist_view(request):
    error = None

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        product_link = request.POST.get('product_link', '').strip()
        notes = request.POST.get('notes', '').strip()
        image = request.FILES.get('photo')

        if not title or not product_link:
            error = 'Title and product link are required'
        else:
            WishlistItem.objects.create(
                user=request.user,
                title=title,
                product_link=product_link,
                notes=notes,
                image=image,
            )
            messages.success(request, 'Wishlist item saved')
            return redirect('wishlist')

    context = {
        'error': error,
        'wishlist_items': request.user.wishlist_items.all(),
    }
    return render(request, 'wishlist.html', context)


@login_required
def my_fashion_view(request):
    error = None

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('photo')

        if not title or not image:
            error = 'A photo and title are required'
        else:
            Outfit.objects.create(
                user=request.user,
                title=title,
                description=description,
                image=image,
            )
            messages.success(request, 'Photo added to your gallery')
            return redirect('dashboard')

    context = {
        'error': error,
        'outfit_count': request.user.outfits.count(),
        'recent_outfits': request.user.outfits.all()[:3],
    }
    return render(request, 'my_fashion.html', context)


@login_required
def toggle_favorite_view(request, outfit_id):
    outfit = get_object_or_404(Outfit, pk=outfit_id, user=request.user)

    if request.method == 'POST':
        outfit.is_favorite = not outfit.is_favorite
        outfit.save(update_fields=['is_favorite'])

    return redirect('gallery')


@login_required
def delete_outfit_view(request, outfit_id):
    outfit = get_object_or_404(Outfit, pk=outfit_id, user=request.user)

    if request.method == 'POST':
        outfit.delete()
        messages.success(request, 'Photo deleted from your gallery')

    return redirect('dashboard')


def logout_view(request):
    logout(request)
    return redirect('login')
