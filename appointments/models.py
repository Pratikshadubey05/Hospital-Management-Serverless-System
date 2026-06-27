from django.db import models
from django.contrib.auth.models import User
# Change the import target from 'Doctor' to 'AvailabilitySlot'
from doctors.models import AvailabilitySlot 

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    
    # This maps the appointment directly to the doctor's specific time slot
    slot = models.OneToOneField(
        AvailabilitySlot, 
        on_delete=models.CASCADE, 
        related_name='appointment_detail'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment: {self.patient.username} with Dr. {self.slot.doctor.username}"