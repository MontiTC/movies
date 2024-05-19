from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CustomLoginView, create_review
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path("", views.index, name="index"),
    path("<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("your_name/", views.get_name, name="get_name"),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('movies/<int:movie_id>/review/', create_review, name='create_review'),
    
    
    ]