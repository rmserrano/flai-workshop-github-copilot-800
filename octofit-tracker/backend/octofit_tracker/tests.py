from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import User, Team, Activity, Leaderboard, Workout


class TeamModelTest(TestCase):
    """Test cases for the Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team for fitness',
            members_count=5,
            total_points=1000
        )
    
    def test_team_creation(self):
        """Test team is created correctly"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.members_count, 5)
        self.assertEqual(self.team.total_points, 1000)
        self.assertIsNotNone(self.team.created_at)
    
    def test_team_string_representation(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class UserModelTest(TestCase):
    """Test cases for the User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='John Doe',
            email='john@example.com',
            team='Test Team'
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.name, 'John Doe')
        self.assertEqual(self.user.email, 'john@example.com')
        self.assertEqual(self.user.team, 'Test Team')
        self.assertIsNotNone(self.user.created_at)
    
    def test_user_string_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'John Doe')
    
    def test_email_unique(self):
        """Test email uniqueness constraint"""
        with self.assertRaises(Exception):
            User.objects.create(
                name='Jane Doe',
                email='john@example.com',
                team='Test Team'
            )


class ActivityModelTest(TestCase):
    """Test cases for the Activity model"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_email='john@example.com',
            activity_type='Running',
            duration=30,
            calories_burned=300,
            distance=5.0,
            date=timezone.now()
        )
    
    def test_activity_creation(self):
        """Test activity is created correctly"""
        self.assertEqual(self.activity.user_email, 'john@example.com')
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories_burned, 300)
        self.assertEqual(self.activity.distance, 5.0)
        self.assertIsNotNone(self.activity.date)
    
    def test_activity_string_representation(self):
        """Test activity string representation"""
        self.assertEqual(str(self.activity), 'john@example.com - Running')


class LeaderboardModelTest(TestCase):
    """Test cases for the Leaderboard model"""
    
    def setUp(self):
        self.entry = Leaderboard.objects.create(
            team_name='Test Team',
            total_points=1500,
            rank=1
        )
    
    def test_leaderboard_creation(self):
        """Test leaderboard entry is created correctly"""
        self.assertEqual(self.entry.team_name, 'Test Team')
        self.assertEqual(self.entry.total_points, 1500)
        self.assertEqual(self.entry.rank, 1)
        self.assertIsNotNone(self.entry.last_updated)
    
    def test_leaderboard_string_representation(self):
        """Test leaderboard string representation"""
        self.assertEqual(str(self.entry), '1. Test Team')


class WorkoutModelTest(TestCase):
    """Test cases for the Workout model"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Morning Cardio',
            description='Start your day with this energizing cardio workout',
            difficulty_level='Intermediate',
            duration=45,
            category='Cardio'
        )
    
    def test_workout_creation(self):
        """Test workout is created correctly"""
        self.assertEqual(self.workout.name, 'Morning Cardio')
        self.assertEqual(self.workout.difficulty_level, 'Intermediate')
        self.assertEqual(self.workout.duration, 45)
        self.assertEqual(self.workout.category, 'Cardio')
        self.assertIsNotNone(self.workout.created_at)
    
    def test_workout_string_representation(self):
        """Test workout string representation"""
        self.assertEqual(str(self.workout), 'Morning Cardio')


class APIEndpointsTest(TestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        # Create test data
        self.team = Team.objects.create(
            name='API Test Team',
            description='Team for API testing',
            members_count=1,
            total_points=500
        )
        
        self.user = User.objects.create(
            name='API Test User',
            email='apitest@example.com',
            team='API Test Team'
        )
    
    def test_api_root_endpoint(self):
        """Test API root endpoint returns correct data"""
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('users', response.json())
        self.assertIn('teams', response.json())
        self.assertIn('activities', response.json())
        self.assertIn('leaderboard', response.json())
        self.assertIn('workouts', response.json())
    
    def test_users_list_endpoint(self):
        """Test users list endpoint"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)
    
    def test_teams_list_endpoint(self):
        """Test teams list endpoint"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)
    
    def test_activities_list_endpoint(self):
        """Test activities list endpoint"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, 200)
    
    def test_leaderboard_list_endpoint(self):
        """Test leaderboard list endpoint"""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, 200)
    
    def test_workouts_list_endpoint(self):
        """Test workouts list endpoint"""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, 200)
