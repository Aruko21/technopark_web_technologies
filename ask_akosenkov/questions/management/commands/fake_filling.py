from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker
import random
from questions.models import *

fake = Faker()


class Command(BaseCommand):
    # описание, которое выводится при выхове команды с ключом --help или при неправильном вводе команды
    help = "Заполнение базы данныъ случайными данными"

    # добавление ключей и аргументов к команде
    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, required=True, help='Количество пользователей для создания')
        parser.add_argument('--questions', type=int, required=True, help='Количество вопросов для создания')
        parser.add_argument('--answers', type=int, required=True, help='Количество ответов для создания')
        parser.add_argument('--tags', type=int, required=True, help='Количество тэгов для создания')
        parser.add_argument('--votes', type=int, help='Количество оценок для создания')

    def handle(self, *args, **kwargs):
        count_users = kwargs['users']
        count_tags = kwargs['tags']
        count_quests = kwargs['questions']
        count_answers = kwargs['answers']
        count_votes = kwargs['votes']

        print("creating profiles...")
        for i in range(count_users):
            random_user = User(username=fake.name(), email=fake.email(), password='111')
            random_user.save()
            random_profile = Profile(user=random_user)
            random_profile.save()

        print("creating tags...")
        for i in range(count_tags):
            random_tag = Tag(title=fake.word())
            random_tag.save()

        profiles = Profile.objects.all()
        tags = Tag.objects.all()

        print("creating questions...")
        for i in range(count_quests):
            print('creating question ', i, '')
            random_profile = random.choice(profiles)
            random_question = Question(title=fake.sentence(), text=fake.text(), author=random_profile)
            random_question.save()
            # print('linking with tags')
            for j in range(random.randint(1, 10)):
                random_tag = random.choice(tags)
                # print('ping before if')
                # Уникальность manytomany и так есть
                # if random_question.tags.all().filter(title=random_tag.title).count() == 0:
                # print('ping after if IN BEGIN')
                # очень долго - может, получится проиндексировать
                random_question.tags.add(random_tag)
                random_tag.rating += 1
                random_tag.save()
                # print('ping after if IN END')
                # print('ping after if')
            random_question.save()

        questions = Question.objects.all()

        print("creating answers...")
        for i in range(count_answers):
            random_profile = random.choice(profiles)
            random_question = random.choice(questions)
            random_answer = Answer(text=fake.text(), author=random_profile, question=random_question)
            random_question.ans_count += 1
            random_question.save()
            random_answer.save()

        answers = Answer.objects.all()

        if count_votes is not None:
            print("creating likes...")
            if count_votes > (questions.count() + answers.count()) * profiles.count():
                random_rating = (questions.count() + answers.count()) * profiles.count() - 1
            else:
                random_rating = count_votes
            random_likes = random.randint(random_rating / 2, random_rating)
            random.shuffle(list(profiles))
            current_likes = 0
            for i in range(random_rating):
                question_or_answer = random.randint(0, 1)
                random_profile = random.choice(profiles)
                if question_or_answer == 0:
                    random_question = random.choice(questions)
                    # заменено на IntegrityError
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
                    # заменено на IntegrityError
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

        print("done")
