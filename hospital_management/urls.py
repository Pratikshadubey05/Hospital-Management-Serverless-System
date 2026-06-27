from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Import the specific views from your appointment app folder
from appointments.views import dashboard_view, initiate_google_auth, google_oauth_callback

def root_redirect(request):
    """
    Catches users entering the empty base domain url path 
    and sends them directly to the main system dashboard.
    """
    return redirect('dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 🌟 FIX: Root path mapping to prevent the 404 empty path error
    path('', root_redirect, name='root_home'),
    
    # Dashboard Routes
    path('patients/dashboard/', dashboard_view, name='dashboard'),
    
    # Google OAuth Routes
    path('auth/google/', initiate_google_auth, name='google_auth'),
    path('auth/google/callback/', google_oauth_callback, name='google_callback'),
    
    # Include urls from your other split apps
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
    path('appointments/', include('appointments.urls')),
    path('accounts/', include
    ('accounts.urls')), # Use this if your folder name is accounts
]