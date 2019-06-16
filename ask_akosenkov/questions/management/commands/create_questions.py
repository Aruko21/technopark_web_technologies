from django.core.management.base import BaseCommand
from faker import Faker
import random
from questions.models import Question, Profile, Tag, Like

fake = Faker()


class Command(BaseCommand):
    # описание, которое выводится при выхове команды с ключом --help или при неправильном вводе команды
    help = "Создание случайных вопрсов"

    # добавление ключей и аргументов к команде
    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Количество вопросов для создания')
        parser.add_argument('--likes', action='store_true', help='Случайное проставление оценок для созданных вопросов')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        is_likes = kwargs['likes']

        profiles = Profile.objects.all()
        tags = Tag.objects.all()

        for i in range(count):
            random_profile = random.choice(profiles)
            random_question = Question(title=fake.sentence(), text=fake.text(), author=random_profile)
            random_question.save()
            for j in range(random.randint(1, 10)):
                random_tag = random.choice(tags)
                # if random_question.tags.all().filter(title=random_tag.title).count() == 0:
                random_question.tags.add(random_tag)
                random_tag.rating += 1
                random_tag.save()
            if is_likes is True:
                random_rating = random.randint(0, profiles.count())
                random_likes = random.randint(0, random_rating)
                random.shuffle(list(profiles))
                current_likes = 0
                for k in range(random_rating):
                    if current_likes <= random_likes:
                        vote = Like(type=Like.LIKE, user=profiles[k], question=random_question)
                        random_question.rating += 1
                        current_likes += 1
                    else:
                        vote = Like(type=Like.DISLIKE, user=profiles[k], question=random_question)
                        random_question.rating -= 1
                    vote.save()
            random_question.save()
