from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import auth
from django import conf
from questions.forms import *
from django.contrib.auth.decorators import login_required
from questions.middleware import CheckProfileMiddleware

from questions.models import *


def pagination(page, object_list):
    # page = request.GET.get('page')

    p = Paginator(object_list, 10)
    try:
        objects_page = p.get_page(page)
        # В документации джанги есть исключение
    except PageNotAnInteger:
        objects_page = p.get_page(1)
    return objects_page


def scroll_answers(answer_id, question_id):
    page_url = ''
    page = 1
    ans_find_id = 0
    # После создания нового ответа нужно заново получить весь список ответов
    answers_list = Answer.objects.sort_by_datetime(question_id)
    ans_page = pagination(page, answers_list)
    while ans_find_id != answer_id and page <= ans_page.paginator.num_pages:
        ans_page = pagination(page, answers_list)
        for ans in ans_page.object_list:
            if ans.id == answer_id:
                page_url = '?page=' + str(page)
                break
        page += 1
    return page_url


def index(request):
    # Чтобы не использовать один и тот же код много раз- можно использовать Middleware
    questions = Question.objects.sort_by_datetime()
    quests_page = pagination(request.GET.get('page'), questions)
    tags = Tag.objects.sort_by_rating()[:20]
    # print("second yo")
    return render(request, 'questions/index.html', context={'object_list': quests_page, 'tags': tags,
                                                            'user': request.profile, 'name': request.username})


def hot(request):
    # prof, username = load_profile(request)
    questions = Question.objects.sort_by_rating()
    quests_page = pagination(request.GET.get('page'), questions)
    tags = Tag.objects.sort_by_rating()[:20]
    return render(request, "questions/hot.html", context={'object_list': quests_page, 'tags': tags,
                                                          'user': request.profile, 'name': request.username})


def ask(request):
    if request.user.is_authenticated:
        tags = Tag.objects.sort_by_rating()[:20]
        if request.method == 'POST':
            form = QuestionForm(request.POST, profile=request.profile)
            if form.is_valid():
                quest = form.save()
                url = "/question/" + str(quest.id)
                return HttpResponseRedirect(url)
        else:
            form = QuestionForm(profile=request.profile)
            return render(request, "questions/ask.html", context={'tags': tags, 'form': form,
                                                                  'user': request.profile, 'name': request.username})
    else:
        return HttpResponseRedirect('%s?continue=%s' % (conf.settings.LOGIN_URL, request.path))


def question(request, question_id):
    try:
        cur_question = Question.objects.get_by_id(question_id)
    except models.ObjectDoesNotExist:
        cur_question = None

    if cur_question is not None:

        answers_page = pagination(request.GET.get('page'), Answer.objects.sort_by_datetime(question_id))
        tags = Tag.objects.sort_by_rating()[:20]
        if request.user.is_authenticated:
            is_auth = True
            if request.method == 'POST':
                form = AnswerForm(request.POST, profile=request.profile, question=cur_question)
                if form.is_valid():
                    answer = form.save()
                    if answers_page.has_other_pages():
                        page_url = scroll_answers(answer.id, question_id)
                    else:
                        page_url = ''

                    url = "/question/" + str(cur_question.id) + '/' + page_url + '#ans' + str(answer.id)
                    return HttpResponseRedirect(url)
            else:
                form = AnswerForm(profile=request.profile, question=cur_question)
        else:
            is_auth = False
            form = None
        return render(request, "questions/question.html", context={'question': cur_question, 'form': form, 'is_auth': is_auth,
                                                                   'object_list': answers_page, 'tags': tags,
                                                                   'user': request.profile, 'name': request.username})
    else:
        # raise - возбуждение исключения
        raise Http404("Following question doesn't exist!")


def tag(request, tag_name):
    try:
        cur_tag = Tag.objects.get_by_name(tag_name)
    except models.ObjectDoesNotExist:
        cur_tag = None

    if cur_tag is not None:
        # prof, username = load_profile(request)
        quests_page = pagination(request.GET.get('page'), Question.objects.get_by_tag(tag_name))
        tags = Tag.objects.sort_by_rating()[:20]
        return render(request, "questions/tag.html", context={'tag_name': tag_name, 'object_list': quests_page,
                                                              'tags': tags, 'user': request.profile,
                                                              'name': request.username})
    else:
        raise Http404("Following tag doesn't exist!")


def login(request):
    tags = Tag.objects.sort_by_rating()[:20]
    if request.method == 'POST':
        form = LoginForm(request.POST)
        url = request.POST.get('continue', '/')
        if form.is_valid():
            user = form.user
            # print("yo")
            auth.login(request, user)
            # print("yo yo")
            if url == conf.settings.LOGIN_URL or url == '/signup/':
                url = '/'
            return HttpResponseRedirect(url)
    else:
        # unbound форма
        form = LoginForm()
        url = request.GET.get('continue', '/')
    return render(request, "questions/login.html", context={'tags': tags, 'form': form,
                                                            'user': None, 'name': None, 'continue_url': url})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.GET.get('continue'))


def signup(request):
    tags = Tag.objects.sort_by_rating()[:20]
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        url = request.POST.get('continue', '/')
        # print('heeeey')
        if form.is_valid():
            # print('yo')
            form.save()
            auth.login(request, form.user)
            return HttpResponseRedirect(url)
    else:
        form = RegisterForm()
        url = request.GET.get('continue', '/')
    return render(request, "questions/signup.html", context={'tags': tags, 'form': form, 'continue_url': url,
                                                             'user': None, 'name': None})


def settings(request):
    if request.user.is_authenticated:
        tags = Tag.objects.sort_by_rating()[:20]
        message = ''
        code = None
        if request.method == 'POST':
            # request передаем, чтобы перезалогинить пользователя в случае смены пароля
            form = SettingsForm(request.POST, request.FILES, user=request.user, request=request,
                                initial={'username': request.user.username, 'first_name': request.user.first_name,
                                         'last_name': request.user.last_name})
            if form.is_valid():
                form.save()
                message = 'Changing success'
                code = 'OK'
                # Нужно обновить информацию об аватарке и нике юзера. Та, что была получена через
                # middleware ранее - уже неактуальна. Так пользователь сможет сразу увидеть изменения
                CheckProfileMiddleware.process_request(CheckProfileMiddleware(None), request)
            else:
                message = 'Changing failed'
                code = 'FAIL'
        else:
            form = SettingsForm(user=request.user, request=request,
                                initial={'username': request.user.username, 'first_name': request.user.first_name,
                                         'last_name': request.user.last_name})
        return render(request, "questions/settings.html", context={'tags': tags, 'user': request.profile, 'form': form,
                                                                   'message': message, 'code': code,
                                                                   'name': request.username})
    else:
        return HttpResponseRedirect('%s?continue=%s' % (conf.settings.LOGIN_URL, request.path))


