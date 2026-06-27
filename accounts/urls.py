from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Standard Django built-in login view that handles form processing automatically
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # Standard logout view
    path('logout/', auth_views.LogoutView.as_view(next_page='root_home'), name='logout'),
]