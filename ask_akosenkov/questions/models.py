from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from questions.managers import *

# Create your models here.


class Profile(models.Model):
    # Но каскад - плохо
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE)
    # Я не уверен насчет width_field
    avatar = models.ImageField(upload_to="static/img/", default="static/img/Arcadia64.jpg")

    def __str__(self):
        return self.user.username

    # objects = ProfileManager()


class Tag(models.Model):
    title = models.CharField(default='', max_length=64, unique=True, verbose_name="Имя тэга")
    rating = models.IntegerField(default=0, verbose_name="Рэйтинг тэга")

    objects = TagManager()

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(default='', max_length=128, verbose_name="Заголовок вопроса")
    text = models.TextField(default='', verbose_name="Тело вопроса")
    rating = models.IntegerField(default=0, verbose_name="Рэйтинг вопроса")
    ans_count = models.IntegerField(default=0, verbose_name="Количество ответов")

    # Понятный идентефикатор
    # slug = models.SlugField(max_length=128, unique=True)

    # auto_now_add - автоматическое заполнение даты при создании нового экземпляра. Если без add - то при обновлении
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания вопроса")

    author = models.ForeignKey(to=Profile, on_delete=models.CASCADE, default=0)

    tags = models.ManyToManyField(to=Tag, blank=True, related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']


class Answer(models.Model):
    text = models.TextField(default='', verbose_name="Тело ответа")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации ответа")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг ответа")

    author = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)

    objects = AnswerManager()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-date']


class Like(models.Model):
    LIKE = "Like"
    DISLIKE = "Dislike"
    VOTE_TYPES = (
        (LIKE, '+'),
        (DISLIKE, '-'),
    )

    type = models.CharField(default=VOTE_TYPES[0][1], max_length=2, choices=VOTE_TYPES)

    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, blank=True, null=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(to=Answer, blank=True, null=True, on_delete=models.CASCADE)

    # objects = LikeManager()

    def __str__(self):
        return self.type

    class Meta:
        unique_together = [['user', 'question'], ['user', 'answer']]
