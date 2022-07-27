from csv import reader

from users.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open('static/data/users.csv', 'r') as csv_file:
            csvf = reader(csv_file)

            for username, password, *__ in csvf:
                user = User(username=username)
                user.set_password(password)

            User.objects.create_user(username=username, email='', password='123')
