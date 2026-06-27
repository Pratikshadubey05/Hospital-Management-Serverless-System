from django.db import models
from django.contrib.auth.models import User

class AvailabilitySlot(models.Model):
    # Only allow users who are classified as doctors to create slots
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Dr. {self.doctor.last_name} - {self.date} ({self.start_time} - {self.end_time})"