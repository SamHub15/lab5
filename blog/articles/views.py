from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import Article
from django.shortcuts import *
from django.http import Http404
from django.contrib import messages

def get_article(request, article_id):
    try:
     post = Article.objects.get(id=article_id)
     return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
     raise Http404

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"],
                'title': request.POST["title"]
            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                # если поля заполнены без ошибок
                Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('get_article', article_id=Article.objects.get(text=form["text"]))
            # перейти на страницу поста
            else:
                # если введенные данные некорректны"
                if Article.objects.filter(title=form["title"]).exists() and not (form["text"]):
                    form['errors'] = u"Название статьи не уникально!"
                else:
                    form['errors'] = u"Заполните все поля!"
                return render(request, 'create_post.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})

    else:
        raise Http404

def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            message = 'Пользователь с таким именем уже существует'
        else:
            User.objects.create_user(username=username, password=password)
            message = 'Вы успешно зарегистрировались!'
        return render(request, 'registration.html', {'message': message})
    else:
        return render(request, 'registration.html')


def auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            message = 'Заполните все поля!'
            return render(request, 'auth.html', {'message': message})

        user = authenticate(request, username=username, password=password)
        if user is None:
            message = 'Неверное имя пользователя или пароль!'
            return render(request, 'auth.html', {'message': message})

        login(request, user)
        return redirect('http://127.0.0.1:8000/')

    return render(request, 'auth.html')


def logout_view(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')


class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path in ['/auth/', '/registration/']:
            return redirect('http://127.0.0.1:8000/')
        response = self.get_response(request)
        return response


