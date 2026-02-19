from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'team', 'created_at']
    list_filter = ['team', 'created_at']
    search_fields = ['name', 'email']
    ordering = ['-created_at']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'members_count', 'total_points', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-total_points']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'activity_type', 'duration', 'calories_burned', 'distance', 'date']
    list_filter = ['activity_type', 'date']
    search_fields = ['user_email']
    ordering = ['-date']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['rank', 'team_name', 'total_points', 'last_updated']
    ordering = ['rank']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'difficulty_level', 'duration', 'category', 'created_at']
    list_filter = ['difficulty_level', 'category']
    search_fields = ['name', 'description']
    ordering = ['name']
