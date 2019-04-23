from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

questions = []
for i in range(1, 22):
    questions.append({
        'title': 'title '+str(i),
        'id': i,
        'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Maiores, sequi?'+str(i),
        'answers': i + 6,
        'rating': i * 100,
        'tag': 'tag' + str(i),
    }
    )

answers = []
for i in range(1, 10):
    answers.append({
        'id': i,
        'text': 'text '+str(i),
        'rating': i * 100,
    }
    )

hot_questions = []
for i in range(1, 20):
    hot_questions.append({
        'title': 'title '+str(i),
        'id': i,
        'com': 'text '+str(i),
        'answers': i + 6,
        'rating': i * 100,
        'tag': 'hot_tag' + str(i),
    }
    )

def pagination(request, object_list, link='/'):
    page = request.GET.get('page')

    p = Paginator(object_list, 10)
    objects_page = p.get_page(page)

    return render(request, link, {'page_obj': objects_page})

# Все файлы ищутся относительно папки templates!
def index(request):
    #return render(request, "questions/index.html",{'questions':questions})
    return pagination(request, questions, 'questions/index.html')

def ask(request):
    return render(request, "questions/ask.html", {})

def question(request, questions_id):
    return render(request, "questions/question.html", {'answers': answers, 'questions_id': questions_id, 'questions': questions})

def tag(request, tag_name):
    return render(request, "questions/tag.html", {'tag_name': tag_name, 'questions': questions})

def login(request):
    return render(request, "questions/login.html", {})

def signup(request):
    return render(request, "questions/signup.html", {})

def settings(request):
    return render(request, "questions/settings.html", {})

def hot(request):
    return pagination(request, hot_questions, 'questions/hot.html')
    #return render(request, "questions/hot.html", {'hot_questions':hot_questions})