from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker
import random
from questions.models import Question, Profile, Answer, Like

fake = Faker()


class Command(BaseCommand):
    # описание, которое выводится при выхове команды с ключом --help или при неправильном вводе команды
    help = "Создание случайных оценок"

    # добавление ключей и аргументов к команде
    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Количество оценок для создания')

    def handle(self, *args, **kwargs):
        count = kwargs['count']

        questions = Question.objects.all()
        answers = Answer.objects.all()
        profiles = Profile.objects.all()

        if count > (questions.count() + answers.count()) * profiles.count():
            random_rating = (questions.count() + answers.count()) * profiles.count() - 1
        else:
            random_rating = count
        random_likes = random.randint(random_rating / 2, random_rating)
        random.shuffle(list(profiles))
        current_likes = 0

        for i in range(random_rating):
            question_or_answer = random.randint(0, 1)
            random_profile = random.choice(profiles)
            if question_or_answer == 0:
                random_question = random.choice(questions)
                # if Like.objects.filter(user=random_profile, question=random_question).count() == 0:
                if current_likes <= random_likes:
                    vote = Like(type=Like.LIKE, user=random_profile, question=random_question)
                    # current_likes += 1
                    # random_question.rating += 1
                    adding_rate = 1
                else:
                    vote = Like(type=Like.DISLIKE, user=random_profile, question=random_question)
                    # random_question.rating -= 1
                    adding_rate = -1
                try:
                    vote.save()
                    random_question.rating += adding_rate
                    if adding_rate > 0:
                        current_likes += 1
                except IntegrityError:
                    pass
                random_question.save()
            else:
                random_answer = random.choice(answers)
                # if Like.objects.filter(user=random_profile, answer=random_answer).count() == 0:
                if current_likes <= random_likes:
                    vote = Like(type=Like.LIKE, user=random_profile, answer=random_answer)
                    # current_likes += 1
                    # random_answer.rating += 1
                    adding_rate = 1
                else:
                    vote = Like(type=Like.DISLIKE, user=random_profile, answer=random_answer)
                    # random_answer.rating -= 1
                    adding_rate = -1
                try:
                    vote.save()
                    random_answer.rating += adding_rate
                    if adding_rate > 0:
                        current_likes += 1
                except IntegrityError:
                    pass
                random_answer.save()
