from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

from questions.models import Profile

fake = Faker()


class Command(BaseCommand):
    # описание, которое выводится при выхове команды с ключом --help или при неправильном вводе команды
    help = "Создание случайных пользователей"

    # добавление ключей и аргументов к команде
    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Количество пользователей для создания')

    def handle(self, *args, **kwargs):
        count = kwargs['count']

        for i in range(count):
            random_user = User(username=fake.name(), email=fake.email(), password='111')
            random_user.save()
            random_profile = Profile(user=random_user)
            random_profile.save()
