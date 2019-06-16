from django.core.management.base import BaseCommand
from faker import Faker
import random
from questions.models import Tag

fake = Faker()


class Command(BaseCommand):
    # описание, которое выводится при выхове команды с ключом --help или при неправильном вводе команды
    help = "Создание случайных тэгов"

    # добавление ключей и аргументов к команде
    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Количество тэгов для создания')

    def handle(self, *args, **kwargs):
        count = kwargs['count']

        for i in range(count):
            random_tag = Tag(title=fake.word())
            random_tag.save()
