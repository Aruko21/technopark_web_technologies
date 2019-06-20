from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from questions.models import *
import re


class LoginForm(forms.Form):
    login = forms.CharField(label='Username', max_length=64,
                            widget=forms.TextInput(attrs={'placeholder': "chloe_price",
                                                          'class': "col-10 form-control"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': "col-10 form-control"}))

    def __init__(self, *args, **kwargs):
        self.user = None
        super(LoginForm, self).__init__(*args, **kwargs)

    # Хорошая практика!
    # ValidationError(
    #     _('Invalid value: %(value)s'),
    #     params={'value': '42'},
    #     code='inv_value',
    # )

    def clean(self):
        login = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')
        if login and password:
            self.user = authenticate(username=login, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    u'Incorrect username and/or password. Try again',
                    code='invalid_login',
                )
        return self.cleaned_data


class QuestionForm(forms.Form):
    title = forms.CharField(label='Title', max_length=64,
                            widget=forms.TextInput(attrs={'placeholder': "Your title",
                                                          'class': "form-control"}))
    body = forms.CharField(label='Question', max_length=1024,
                           widget=forms.Textarea(attrs={'placeholder': "Type your question here",
                                                        'class': "form-control"}))
    tags = forms.CharField(label='Tags', max_length=128, required=False,
                           widget=forms.TextInput(attrs={'placeholder': "Example: Amberprice Pricefield Love",
                                                         'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile')
        super(QuestionForm, self).__init__(*args, **kwargs)

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        regular = re.compile(r'[A-Za-zА-Яа-я ]+')
        result = regular.search(tags).group(0)
        if len(tags) != len(result):
            raise forms.ValidationError(
                u'Use only letters and spaces',
                code='invalid_tags',
            )
        tag_list = tags.split()
        for tag in tag_list:
            if len(tag) <= 2:
                raise forms.ValidationError(
                    u'Tag %(tag)s is too short',
                    code='short_tag',
                    params={'tag': tag}
                )
        return tag_list

    def save(self):
        title = self.cleaned_data.get('title')
        body = self.cleaned_data.get('body')
        tags = self.cleaned_data.get('tags')
        quest = Question(title=title, text=body, author=self.profile)
        quest.save()
        for tag in tags:
            tag_model = Tag.objects.get_or_create(title=tag)
            print("TAG IS: ", tag_model)
            tag_model[0].rating += 1
            tag_model[0].save()
            quest.tags.add(tag_model[0])
        quest.save()
        return quest


class AnswerForm(forms.Form):
    body = forms.CharField(label='Your answer', max_length=1024,
                           widget=forms.Textarea(attrs={'placeholder': "Type your answer here",
                                                        'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile')
        self.question = kwargs.pop('question')
        super(AnswerForm, self).__init__(*args, **kwargs)

    def save(self):
        body = self.cleaned_data.get('body')
        answer = Answer(text=body, author=self.profile, question=self.question)
        answer.save()
        self.question.ans_count += 1
        self.question.save()
        return answer


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=64,
                               widget=forms.TextInput(attrs={'placeholder': "chloe_price",
                                                             'class': "form-control"}))
    email = forms.EmailField(label="Your e-mail", widget=forms.EmailInput(attrs={'class': "form-control",
                                                                                 'placeholder': "example@gmail.com"}))
    password1 = forms.CharField(label="Your password", widget=forms.PasswordInput(attrs={'class': "form-control"}))
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={'class': "form-control"}),
                                help_text="Enter the same password as above, for verification.")

    avatar = forms.ImageField(label='Your avatar', required=False, widget=forms.FileInput(attrs={'class': "form-control-file"}))

    def __init__(self, *args, **kwargs):
        self.user = None
        super(RegisterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        self.user = User(username=self.cleaned_data.get('username'), email=self.cleaned_data.get('email'))
        self.user.set_password(self.cleaned_data.get('password1'))
        self.user.save()
        avatar = self.cleaned_data.get('avatar')
        print("psss: ", avatar)
        if avatar:
            prof = Profile(user=self.user, avatar=avatar)
        else:
            prof = Profile(user=self.user)
        prof.save()
        return prof


class SettingsForm(UserChangeForm):

    username = forms.CharField(label='Username', max_length=64, required=False,
                               widget=forms.TextInput(attrs={'class': "form-control"}))
    first_name = forms.CharField(label="First Name", required=False, max_length=32,
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(label="Last Name", required=False, max_length=32,
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(label="New password", required=False, widget=forms.PasswordInput(attrs={'class': "form-control"}))
    password2 = forms.CharField(label="Password confirmation", required=False,
                                widget=forms.PasswordInput(attrs={'class': "form-control"}),
                                help_text="Enter the same password as above, for verification.")
    password = forms.CharField(label="Current password", widget=forms.PasswordInput(attrs={'class': "form-control"}))
    avatar = forms.ImageField(label='New avatar', required=False, widget=forms.FileInput(attrs={'class': "form-control-file"}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.request = kwargs.pop('request')
        # self.user = None
        # Важно корректно использовать метод super! Нельзя передавать self - будет больно
        super(SettingsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'password')

    def clean_password(self):
        login = self.user.username
        password = self.cleaned_data.get('password')
        if login and password:
            check_user = authenticate(username=login, password=password)
            if check_user is None:
                raise forms.ValidationError(
                    u'Incorrect password',
                    code='invalid_pass',
                )
        super(SettingsForm, self).clean_password()
        return password

    def clean_last_name(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        if first_name == '':
            raise forms.ValidationError(
                u"Can't set last name without first name",
                code='miss_first_name',
            )
        return last_name

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password1')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        avatar = self.cleaned_data.get('avatar')
        if username == self.user.username:
            self.cleaned_data['username'] = ''
            username = ''
        if first_name == self.user.first_name:
            self.cleaned_data['first_name'] = ''
            first_name = ''
        if last_name == self.user.last_name:
            self.cleaned_data['last_name'] = ''
            last_name = ''
        if username == '' and password == '' and first_name == '' and last_name == '' and not avatar:
            raise forms.ValidationError(
                u'Enter at least one field, that you want to change',
                code="empty_data",
            )
        super(SettingsForm, self).clean()
        return self.cleaned_data

    def save(self, commit=True):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password1')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        avatar = self.cleaned_data.get('avatar')

        if username and username != self.user.username:
            self.user.username = username
        if password:
            self.user.set_password(password)
            login(self.request, self.user)
        if first_name and first_name != self.user.first_name:
            self.user.first_name = first_name
        if last_name and last_name != self.user.last_name:
            self.user.last_name = last_name
        if avatar:
            profile = Profile.objects.get(user=self.user)
            profile.avatar = avatar
            # TODO: сделать удаление предыдущей аватарки
            profile.save()
        self.user.save()
        return self.user

