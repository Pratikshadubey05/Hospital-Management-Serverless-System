from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Looks for your login form template inside registration/templates/registration/login.html
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # Standard logout route
    path('logout/', auth_views.LogoutView.as_view(next_page='root_home'), name='logout'),
]