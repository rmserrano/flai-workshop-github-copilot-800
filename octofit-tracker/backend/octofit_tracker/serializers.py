from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId


class ObjectIdField(serializers.Field):
    """Custom field to handle MongoDB ObjectId"""
    def to_representation(self, value):
        return str(value)
    
    def to_internal_value(self, data):
        try:
            return ObjectId(data)
        except:
            raise serializers.ValidationError("Invalid ObjectId")


class UserSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    
    class Meta:
        model = User
        fields = ['_id', 'name', 'email', 'team', 'created_at']


class TeamSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'members_count', 'total_points', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    
    class Meta:
        model = Activity
        fields = ['_id', 'user_email', 'activity_type', 'duration', 'calories_burned', 'distance', 'date', 'created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['_id', 'team_name', 'total_points', 'rank', 'last_updated']


class WorkoutSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    
    class Meta:
        model = Workout
        fields = ['_id', 'name', 'description', 'difficulty_level', 'duration', 'category', 'created_at']
