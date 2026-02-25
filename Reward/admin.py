from django.contrib import admin
from .models import RewardProfile, RewardHistory


@admin.register(RewardProfile)
class RewardProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'level', 'badge')
    search_fields = ('user__email',)
    list_filter = ('level', 'badge')


@admin.register(RewardHistory)
class RewardHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'points', 'created_at')
    search_fields = ('user__email', 'action')
    list_filter = ('created_at',)
