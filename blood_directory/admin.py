from django.contrib import admin
from .models import UserProfile, EmergencyRequest, DonationHistory


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'first_name',
        'last_name',
        'blood_group',
        'district',
        'upazila',
        'is_available'
    )
    search_fields = ('user__email', 'first_name', 'last_name', 'phone')
    list_filter = ('blood_group', 'district', 'is_available')


@admin.register(EmergencyRequest)
class EmergencyRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'requester',
        'blood_group',
        'district',
        'status',
        'assigned_donor',
        'created_at'
    )
    search_fields = ('requester__email', 'blood_group', 'district')
    list_filter = ('status', 'blood_group', 'district')
    ordering = ('-created_at',)


@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'donor',
        'emergency_request',
        'donation_date',
        'next_eligible_date'
    )
    search_fields = ('donor__email',)
    list_filter = ('donation_date',)
    ordering = ('-donation_date',)
