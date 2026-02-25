from django.db import models
from user.models import User
from django.utils import timezone

class UserProfile(models.Model):
    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("O+", "O+"), ("O-", "O-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    district = models.CharField(max_length=100)
    upazila = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    last_donation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.blood_group})"
    



class EmergencyRequest(models.Model):
    STATUS_CHOICES = [
        ("Open","Open"),
        ("assigned","assigned"),
        ("closed","closed"),
    ]
    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requests"
    )
    blood_group = models.CharField(max_length=5)
    district = models.CharField(max_length=100)
    upazila = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="open"
    )
    assigned_donor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_requests",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request #{self.id} - {self.blood_group}"
    


class DonationHistory(models.Model):
    donor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="donations"
    )
    emergency_request = models.ForeignKey(
        EmergencyRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    donation_date = models.DateField(default=timezone.now)
    next_eligible_date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.donor.email} - {self.donation_date}"
