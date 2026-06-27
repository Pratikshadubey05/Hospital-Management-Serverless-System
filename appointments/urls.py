from django.urls import path
from . import views

urlpatterns = [
    # 📊 Core Application Dashboard Workspace Router
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # 🌟 FIXED ACTION: Triggers your microservice booking & email notification logic
    path('patients/book/<int:slot_id>/', views.book_appointment_view, name='book_appointment'),
    
    # 🌐 Google Authentication Calendar Framework Routers
    path('connect-calendar/', views.initiate_google_auth, name='connect_calendar'),
    path('oauth2callback/', views.google_oauth_callback, name='google_oauth_callback'),
]