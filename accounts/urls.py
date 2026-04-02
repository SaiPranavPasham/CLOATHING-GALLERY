from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('gallery/', views.dashboard_view, name='gallery'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('my-fashion/', views.my_fashion_view, name='my_fashion'),
    path('outfits/<int:outfit_id>/favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    path('outfits/<int:outfit_id>/delete/', views.delete_outfit_view, name='delete_outfit'),
    path('logout/', views.logout_view, name='logout'),
]
