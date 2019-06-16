from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.http import HttpResponse, Http404

from questions.models import *

# questions = []
# for i in range(1, 22):
#     questions.append({
#         'title': 'title '+str(i),
#         'id': i,
#         'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Maiores, sequi?'+str(i),
#         'answers': i + 6,
#         'rating': i * 100,
#         'tag': 'tag' + str(i),
#     }
#     )
#
# answers = []
# for i in range(1, 10):
#     answers.append({
#         'id': i,
#         'text': 'text '+str(i),
#         'rating': i * 100,
#     }
#     )
#
# hot_questions = []
# for i in range(1, 20):
#     hot_questions.append({
#         'title': 'title '+str(i),
#         'id': i,
#         'com': 'text '+str(i),
#         'answers': i + 6,
#         'rating': i * 100,
#         'tag': 'hot_tag' + str(i),
#     }
#     )


def pagination(page, object_list):
    # page = request.GET.get('page')

    p = Paginator(object_list, 10)
    try:
        objects_page = p.get_page(page)
        # В документации джанги есть исключение
    except PageNotAnInteger:
        objects_page = p.get_page(1)
    return objects_page


# Все файлы ищутся относительно папки templates!
def index(request):
    questions = Question.objects.sort_by_datetime()
    quests_page = pagination(request.GET.get('page'), questions)
    tags = Tag.objects.sort_by_rating()[:20]

    return render(request, 'questions/index.html', context={'object_list': quests_page, 'tags': tags})


def hot(request):
    questions = Question.objects.sort_by_rating()
    quests_page = pagination(request.GET.get('page'), questions)
    tags = Tag.objects.sort_by_rating()[:20]
    return render(request, "questions/hot.html", context={'object_list': quests_page, 'tags': tags})


def ask(request):
    tags = Tag.objects.sort_by_rating()[:20]
    return render(request, "questions/ask.html", context={'tags': tags})


def question(request, question_id):
    try:
        cur_question = Question.objects.get_by_id(question_id)
    except models.ObjectDoesNotExist:
        cur_question = None

    if cur_question is not None:
        answers_page = pagination(request.GET.get('page'), Answer.objects.sort_by_datetime(question_id))
        tags = Tag.objects.sort_by_rating()[:20]
        return render(request, "questions/question.html", context={'question': cur_question, 'object_list': answers_page, 'tags': tags})
    else:
        # raise - возбуждение исключения
        raise Http404("Following question doesn't exist!")


def tag(request, tag_name):
    try:
        cur_tag = Tag.objects.get_by_name(tag_name)
    except models.ObjectDoesNotExist:
        cur_tag = None

    if cur_tag is not None:
        quests_page = pagination(request.GET.get('page'), Question.objects.get_by_tag(tag_name))
        tags = Tag.objects.sort_by_rating()[:20]
        return render(request, "questions/tag.html", context={'tag_name': tag_name, 'object_list': quests_page, 'tags': tags})
    else:
        raise Http404("Following tag doesn't exist!")


def login(request):
    tags = Tag.objects.sort_by_rating()[:20]
    return render(request, "questions/login.html", context={'tags': tags})


def signup(request):
    tags = Tag.objects.sort_by_rating()[:20]
    return render(request, "questions/signup.html", context={'tags': tags})


def settings(request):
    tags = Tag.objects.sort_by_rating()[:20]
    return render(request, "questions/settings.html", context={'tags': tags})

