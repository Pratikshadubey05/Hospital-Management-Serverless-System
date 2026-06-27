import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .forms import PatientForm
from .models import Patient
from doctors.models import AvailabilitySlot
from appointments.models import Appointment

# =======================================================
# 🔒 SECURITY ACCESS CONTROL DECORATOR
# =======================================================
def patient_required(view_func):
    """Ensures only users with the 'patient' role can interact with booking logic."""
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'patient':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("Access denied. This section is restricted to registered patients.")
    return wrap


# =======================================================
# 📅 HOSPITAL CORE FUNCTIONALITIES (DASHBOARD & SECURE BOOKING)
# =======================================================

@login_required
@patient_required
def patient_dashboard(request):
    """Displays all upcoming, unbooked doctor availability slots to the patient."""
    today = datetime.date.today()
    # Fetch all open time slots from today onward
    available_slots = AvailabilitySlot.objects.filter(
        is_booked=False, 
        date__gte=today
    ).order_by('date', 'start_time')
    
    return render(request, 'dashboard.html', {'slots': available_slots})


@login_required
@patient_required
@transaction.atomic
def book_appointment(request, slot_id):
    """
    Safely handles booking submissions.
    Uses database row-level locking via select_for_update() to prevent race conditions.
    """
    # select_for_update() locks the selected slot row until this transaction block commits
    slot = get_object_or_404(AvailabilitySlot.objects.select_for_update(), id=slot_id)
    
    # Gracefully intercept concurrent race condition attempts
    if slot.is_booked:
        messages.error(request, "This appointment slot was just taken by another patient.")
        return redirect('patient_dashboard')
    
    # Mark slot locked immediately
    slot.is_booked = True
    slot.save()
    
    # Create concrete appointment registration
    Appointment.objects.create(patient=request.user, slot=slot)
    
    # TODO: Trigger Google Calendar OAuth & Local Serverless HTTP endpoint here
    
    messages.success(request, f"Appointment with Dr. {slot.doctor.username} has been successfully secured!")
    return redirect('patient_dashboard')


# =======================================================
# 👥 PRE-EXISTING ADMINISTRATIVE PATIENT CRUD MANAGEMENT
# =======================================================

# ✅ LIST ALL PATIENTS
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})


# ✅ ADD PATIENT
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'patients/add_patient.html', {'form': form})


# ✅ EDIT PATIENT
def edit_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/edit_patient.html', {'form': form})


# ✅ DELETE PATIENT
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patients/delete_patient.html', {'patient': patient})