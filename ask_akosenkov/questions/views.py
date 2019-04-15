from django.conf.urls import url

from questions.views import AboutView

urlpatterns = [
    url(r'^about$', AboutView.as_view(), name='about'),
]
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "about.html"

def quetions_list(request):
    return render(
        request,
        'questions_list.html',
        {'questions': #smth }
    )
