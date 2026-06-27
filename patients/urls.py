from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('add/', views.add_patient, name='add_patient'),
    path('edit/<int:id>/', views.edit_patient, name='edit_patient'),
    path('delete/<int:id>/', views.delete_patient, name='delete_patient'),
    # New Dashboard and Core Booking Flow endpoints
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('book/<int:slot_id>/', views.book_appointment, name='book_appointment'),
]