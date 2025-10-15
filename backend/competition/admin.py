from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Submission, User, Vote


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Competition Info', {'fields': ('team', 'points')}),
    )
    list_display = ('username', 'email', 'team', 'points', 'is_staff')
    list_filter = DjangoUserAdmin.list_filter + ('team',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'true_identity', 'created_at')
    list_filter = ('category', 'true_identity', 'created_at')
    search_fields = ('title', 'description', 'author__username')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('submission', 'voter', 'guess', 'created_at')
    list_filter = ('guess', 'created_at')
    search_fields = ('submission__title', 'voter__username')
