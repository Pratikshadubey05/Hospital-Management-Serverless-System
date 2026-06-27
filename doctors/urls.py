from django.urls import path
from . import views

urlpatterns = [
    # Route for the main doctor control panel workspace dashboard
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
]