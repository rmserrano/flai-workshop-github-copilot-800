from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from pymongo import MongoClient
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        
        # Delete all existing data using Django ORM
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared!'))
        
        # Create unique index on email field
        self.stdout.write(self.style.WARNING('Creating unique index on email field...'))
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.users.create_index([("email", 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Unique index created!'))
        
        # Create Teams
        self.stdout.write(self.style.WARNING('Creating teams...'))
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes united for fitness glory',
            members_count=0,
            total_points=0
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='The Justice League striving for superhuman fitness',
            members_count=0,
            total_points=0
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created {Team.objects.count()} teams'))
        
        # Create Marvel users
        marvel_heroes = [
            {'name': 'Tony Stark', 'email': 'ironman@marvel.com'},
            {'name': 'Steve Rogers', 'email': 'captain@marvel.com'},
            {'name': 'Thor Odinson', 'email': 'thor@marvel.com'},
            {'name': 'Natasha Romanoff', 'email': 'blackwidow@marvel.com'},
            {'name': 'Bruce Banner', 'email': 'hulk@marvel.com'},
            {'name': 'Peter Parker', 'email': 'spiderman@marvel.com'},
            {'name': 'Wanda Maximoff', 'email': 'scarletwitch@marvel.com'},
            {'name': 'T\'Challa', 'email': 'blackpanther@marvel.com'},
        ]
        
        # Create DC users
        dc_heroes = [
            {'name': 'Clark Kent', 'email': 'superman@dc.com'},
            {'name': 'Bruce Wayne', 'email': 'batman@dc.com'},
            {'name': 'Diana Prince', 'email': 'wonderwoman@dc.com'},
            {'name': 'Barry Allen', 'email': 'flash@dc.com'},
            {'name': 'Arthur Curry', 'email': 'aquaman@dc.com'},
            {'name': 'Hal Jordan', 'email': 'greenlantern@dc.com'},
            {'name': 'Victor Stone', 'email': 'cyborg@dc.com'},
            {'name': 'Oliver Queen', 'email': 'greenarrow@dc.com'},
        ]
        
        self.stdout.write(self.style.WARNING('Creating users...'))
        marvel_users = []
        for hero in marvel_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team='Team Marvel'
            )
            marvel_users.append(user)
        
        dc_users = []
        for hero in dc_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team='Team DC'
            )
            dc_users.append(user)
        
        # Update team member counts
        team_marvel.members_count = len(marvel_users)
        team_marvel.save()
        team_dc.members_count = len(dc_users)
        team_dc.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {User.objects.count()} users'))
        
        # Create Activities
        self.stdout.write(self.style.WARNING('Creating activities...'))
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'Martial Arts']
        
        all_users = marvel_users + dc_users
        for user in all_users:
            # Create 3-5 activities per user
            for _ in range(random.randint(3, 5)):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)  # 20-120 minutes
                calories = duration * random.randint(5, 12)
                distance = round(random.uniform(2, 20), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                days_ago = random.randint(0, 30)
                
                Activity.objects.create(
                    user_email=user.email,
                    activity_type=activity_type,
                    duration=duration,
                    calories_burned=calories,
                    distance=distance,
                    date=timezone.now() - timedelta(days=days_ago)
                )
        
        self.stdout.write(self.style.SUCCESS(f'Created {Activity.objects.count()} activities'))
        
        # Calculate team points
        marvel_points = sum(
            activity.calories_burned 
            for activity in Activity.objects.filter(user_email__in=[u.email for u in marvel_users])
        )
        dc_points = sum(
            activity.calories_burned 
            for activity in Activity.objects.filter(user_email__in=[u.email for u in dc_users])
        )
        
        team_marvel.total_points = marvel_points
        team_marvel.save()
        team_dc.total_points = dc_points
        team_dc.save()
        
        # Create Leaderboard
        self.stdout.write(self.style.WARNING('Creating leaderboard...'))
        teams_sorted = [
            {'name': 'Team Marvel', 'points': marvel_points},
            {'name': 'Team DC', 'points': dc_points}
        ]
        teams_sorted.sort(key=lambda x: x['points'], reverse=True)
        
        for idx, team in enumerate(teams_sorted, start=1):
            Leaderboard.objects.create(
                team_name=team['name'],
                total_points=team['points'],
                rank=idx
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {Leaderboard.objects.count()} leaderboard entries'))
        
        # Create Workouts
        self.stdout.write(self.style.WARNING('Creating workout suggestions...'))
        workouts = [
            {
                'name': 'Super Soldier Strength Training',
                'description': 'Captain America\'s legendary strength workout combining push-ups, pull-ups, and core exercises',
                'difficulty_level': 'Advanced',
                'duration': 60,
                'category': 'Strength'
            },
            {
                'name': 'Asgardian Hammer Swings',
                'description': 'Thor-inspired kettlebell workout for explosive power and endurance',
                'difficulty_level': 'Expert',
                'duration': 45,
                'category': 'Power'
            },
            {
                'name': 'Spider-Sense Agility Circuit',
                'description': 'Quick reflexes and agility training inspired by Spider-Man\'s acrobatic style',
                'difficulty_level': 'Intermediate',
                'duration': 40,
                'category': 'Agility'
            },
            {
                'name': 'Black Widow Combat Cardio',
                'description': 'High-intensity martial arts-inspired cardio workout',
                'difficulty_level': 'Advanced',
                'duration': 50,
                'category': 'Cardio'
            },
            {
                'name': 'Flash Speed Training',
                'description': 'Lightning-fast sprint intervals to build speed and endurance',
                'difficulty_level': 'Intermediate',
                'duration': 30,
                'category': 'Speed'
            },
            {
                'name': 'Wonder Woman Warrior Workout',
                'description': 'Amazon warrior-inspired full-body strength and combat training',
                'difficulty_level': 'Advanced',
                'duration': 55,
                'category': 'Strength'
            },
            {
                'name': 'Batman Tactical Training',
                'description': 'Dark Knight\'s strategic workout combining strength, stealth, and endurance',
                'difficulty_level': 'Expert',
                'duration': 70,
                'category': 'Mixed'
            },
            {
                'name': 'Aquaman Ocean Swim',
                'description': 'Endurance swimming workout for building stamina and core strength',
                'difficulty_level': 'Beginner',
                'duration': 35,
                'category': 'Cardio'
            },
            {
                'name': 'Hulk Smash Power Lifting',
                'description': 'Heavy compound lifts for maximum strength gains',
                'difficulty_level': 'Expert',
                'duration': 60,
                'category': 'Strength'
            },
            {
                'name': 'Green Arrow Archery Core',
                'description': 'Core stability and shoulder strengthening workout',
                'difficulty_level': 'Beginner',
                'duration': 30,
                'category': 'Core'
            },
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {Workout.objects.count()} workouts'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'Teams: {Team.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Activities: {Activity.objects.count()}')
        self.stdout.write(f'Leaderboard entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Workouts: {Workout.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*50))
