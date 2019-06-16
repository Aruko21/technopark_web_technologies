from django.core.management.base import BaseCommand
from faker import Faker
import random
from questions.models import Question, Profile, Answer, Like

fake = Faker()


class Command(BaseCommand):
    # описание, которое выводится при выхове команды с ключом --help или при неправильном вводе команды
    help = "Создание случайных ответов"

    # добавление ключей и аргументов к команде
    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Количество ответов для создания')
        parser.add_argument('--likes', action='store_true', help='Случайное проставление оценок для созданных ответов')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        is_likes = kwargs['likes']

        questions = Question.objects.all()
        profiles = Profile.objects.all()

        for i in range(count):
            random_profile = random.choice(profiles)
            random_question = random.choice(questions)
            random_answer = Answer(text=fake.text(), author=random_profile, question=random_question)
            random_question.ans_count += 1
            random_question.save()
            random_answer.save()

            if is_likes is True:
                random_rating = random.randint(0, profiles.count())
                random_likes = random.randint(0, random_rating)
                random.shuffle(list(profiles))
                current_likes = 0
                for k in range(random_rating):
                    if current_likes <= random_likes:
                        vote = Like(type=Like.LIKE, user=profiles[k], answer=random_answer)
                        random_answer.rating += 1
                        current_likes += 1
                    else:
                        vote = Like(type=Like.DISLIKE, user=profiles[k], answer=random_answer)
                        random_answer.rating -= 1
                    vote.save()
            random_answer.save()
