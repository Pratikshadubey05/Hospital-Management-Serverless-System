from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import AvailabilitySlot
from .forms import AvailabilitySlotForm

def doctor_required(view_func):
    """Custom decorator to ensure only logged-in doctors can access views."""
    def wrap(request, *args, **kwargs):
        # Assumes request.user.profile.role setup. If profile structure differs, 
        # change to match how you flag a user as a doctor.
        if hasattr(request.user, 'profile') and request.user.profile.role == 'doctor':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("Access denied. This dashboard is for doctors only.")
    return wrap

@login_required
@doctor_required
def doctor_dashboard(request):
    # Fetch all slots belonging to the logged-in doctor
    slots = AvailabilitySlot.objects.filter(doctor=request.user).order_by('date', 'start_time')
    
    if request.method == 'POST':
        form = AvailabilitySlotForm(request.POST)
        if form.is_valid():
            # Create slot instance without saving to DB immediately so we can assign the doctor
            slot = form.save(commit=False)
            slot.doctor = request.user
            slot.save()
            messages.success(request, "Availability slot added successfully!")
            return redirect('doctor_dashboard')
    else:
        form = AvailabilitySlotForm()
        
    context = {
        'slots': slots,
        'form': form
    }
    return render(request, 'doctors/dashboard.html', context)