from django.db import models

# Create your models here.

class Question(models.Model):
    questionText = models.CharField(max_length = 200)
    publicationDate = models.DateTimeField('published date')
    def __str__(self):
        return self.questionText

# class User():
# class Tag():