from django.urls import path

from questions.views import AboutView

urlpatterns = [
    path('about', AboutView.as_view(), name='about'),
    path('questions', questions-list, name='questions-list'),
]

