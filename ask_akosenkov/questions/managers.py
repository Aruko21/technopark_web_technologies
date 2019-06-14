from django.db import models

# class ProfileManager(models.Manager):
#     '''some'''


class QuestionManager(models.Manager):
    def sort_by_rating(self):
        return self.all().order_by('rating').reverse()

    def sort_by_datetime(self):
        return self.all()

    def get_by_id(self, quest_id):
        return self.get(id=quest_id)

    def get_by_tag(self, tag_name):
        return self.filter(tags__title=tag_name).order_by('rating').reverse()


class AnswerManager(models.Manager):
    def sort_by_datetime(self, quest_id):
        return self.filter(question__id=quest_id)

    def sort_by_rating(self, quest_id):
        return self.filter(question__id=quest_id).order_by('rating').reverse()


class TagManager(models.Manager):
    def sort_by_rating(self):
        return self.all().order_by('rating').reverse()

    def get_by_name(self, tag_name):
        return self.get(title=tag_name)


# class LikeManager(models.Manager):
#     '''some'''
