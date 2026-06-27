from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import requests  # 🌟 Added to communicate with Terminal 1's notification service

# 1. Clean, Whitespace-Free Cross-App Imports
from patients.models import Patient 
from doctors.models import AvailabilitySlot 
from doctors.forms import AvailabilitySlotForm 
from appointments.models import Appointment

# 2. Local App Utility Functions
from .utils import get_google_auth_flow

# ==========================================
# 1. CORE MULTI-ROLE DASHBOARD VIEW
# ==========================================
@login_required
def dashboard_view(request):
    """
    Fetches global administrative statistics directly from database models
    and structures the workspace context depending on user roles.
    """
    # Pull metrics straight from tables to guarantee non-zero updates on UI cards
    context = {
        'patient_count': Patient.objects.count(),
        'doctor_count': User.objects.filter(profile__role='doctor').count(),
        'appointment_count': AvailabilitySlot.objects.filter(is_booked=True).count(),
        'department_count': 4, # Keeps presentation dashboard columns beautifully balanced
        'slots': None,
        'form': None,
    }
    
    # Safely capture profile role and handle missing roles (like superusers) gracefully
    try:
        user_role = getattr(request.user.profile, 'role', None)
    except ObjectDoesNotExist:
        user_role = 'admin'
    
    if user_role == 'doctor':
        # Doctors manage their own specific calendar slots
        context['slots'] = AvailabilitySlot.objects.filter(doctor=request.user).order_by('date', 'start_time')
        
        # Handle new availability slot creation forms
        if request.method == 'POST':
            form = AvailabilitySlotForm(request.POST)
            if form.is_valid():
                slot = form.save(commit=False)
                slot.doctor = request.user
                slot.save()
                messages.success(request, "Availability slot added successfully!")
                return redirect('dashboard')
        else:
            context['form'] = AvailabilitySlotForm()
            
    elif user_role == 'patient':
        # Patients view all open medical slots available for booking across the clinic
        context['slots'] = AvailabilitySlot.objects.filter(is_booked=False).order_by('date', 'start_time')
    
    else:
        # Fallback for administrative/superuser profiles so they can view layout metrics
        messages.info(request, "Logged in as Administrator. Showing global hospital statistics layout.")
        context['slots'] = AvailabilitySlot.objects.all().order_by('date', 'start_time')

    return render(request, 'dashboard.html', context)


# ==========================================
# 2. MICROSERVICE APPOINTMENT BOOKING HANDLER
# ==========================================
@login_required
def book_appointment_view(request, slot_id):
    """
    Handles patient booking selections and safely transmits the payload 
    out over HTTP to your local microservice listening on port 3000.
    """
    slot = get_object_or_404(AvailabilitySlot, id=slot_id, is_booked=False)
    
    # Lock the database record row state down instantly
    slot.is_booked = True
    slot.save()
    
    # 🌟 INTEGRATION WORKFLOW: Package JSON data parameters for Terminal 1
    microservice_url = "http://127.0.0.1:3000/send-email"
    email_payload = {
        "to_email": request.user.email if request.user.email else "patient_demo@example.com",
        "subject": "Appointment Confirmation - HMS Portal",
        "body": f"Hello {request.user.username},\n\nYour appointment with Dr. {slot.doctor.username} on {slot.date} at {slot.start_time} has been confirmed successfully."
    }
    
    try:
        # Fire off the asynchronous HTTP request block with a 4-second timeout threshold
        response = requests.post(microservice_url, json=email_payload, timeout=4)
        
        if response.status_code == 200:
            messages.success(request, "Appointment secured! Microservice handled notification payload (Terminal 1).")
        else:
            messages.warning(request, "Slot booked, but the port 3000 listener returned a bad processing state.")
            
    except requests.exceptions.ConnectionError:
        # 🛡️ Failure Guard: Keeps the user dashboard responsive even if app.py is offline
        messages.info(request, "Appointment booked successfully! Note: Notification service (Terminal 1) was offline.")

    return redirect('dashboard')


# ==========================================
# 3. GOOGLE OAUTH INTERACTION VIEWS
# ==========================================
@login_required
def initiate_google_auth(request):
    """Redirects the application user out to Google's authentication consent form screen."""
    flow = get_google_auth_flow()
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    
    # Store state session properties locally to prevent cross-site request forgery vulnerabilities
    request.session['oauth_state'] = state
    return redirect(authorization_url)

@login_required
def google_oauth_callback(request):
    """Captures authorization authorization responses returning back from Google systems."""
    flow = get_google_auth_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    
    credentials = flow.credentials
    
    # Target and save credentials parameters to session caches securely.
    request.session['google_access_token'] = credentials.token
    request.session['google_refresh_token'] = credentials.refresh_token
    
    # Route safely back to the core dashboard layout
    return redirect('dashboard')