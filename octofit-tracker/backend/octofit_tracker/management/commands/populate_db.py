from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all users
        User.objects.all().delete()
        # Create Marvel and DC teams
        teams = [
            {'name': 'Marvel', 'members': ['Iron Man', 'Captain America', 'Thor', 'Black Widow']},
            {'name': 'DC', 'members': ['Superman', 'Batman', 'Wonder Woman', 'Flash']}
        ]
        # Create users
        for team in teams:
            for hero in team['members']:
                email = f"{hero.replace(' ', '').lower()}@{team['name'].lower()}.com"
                User.objects.create(username=hero, email=email)
        # Activities, leaderboard, workouts collections can be created similarly if models exist
        self.stdout.write(self.style.SUCCESS('Test users and teams created.'))
        # Ensure unique index on email using pymongo
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db['users'].create_index('email', unique=True)
        self.stdout.write(self.style.SUCCESS('Unique index on email ensured.'))
