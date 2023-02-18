from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta
from django.contrib.auth.models import User, AnonymousUser

from .models import Post, Category, Response
from .forms import PostForm, ResponseForm
from .models import Author
from GamesPortal.settings import DAILY_POST_LIMIT

class PostsList(ListView):
    queryset = Post.objects.all()  # Post.news)
    ordering = '-created'
    template_name = 'board/posts_list.html'
    context_object_name = 'posts'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # момент на сутки назад
        prev_day = datetime.utcnow() - timedelta(days=1)
        # количество постов с этого момента
        user = self.request.user
        if not isinstance(self.request.user, AnonymousUser):
            posts_day_count = posts_day_count = Post.objects.filter(created__gte=prev_day, author__author=user).count()
            context['allow_post'] = (posts_day_count < DAILY_POST_LIMIT)
        else:
            context['allow_post'] = False
        # К словарю добавим количество всех новостей, чтобы не резало пагинатором
        context['posts_amount'] = len(self.queryset)
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новости
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'board/post.html'
    # Название объекта, в котором будет выбранная новость
    context_object_name = 'post'


# Добавляем новое представление для создания поста.
class PostCreate(LoginRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель объявлений
    model = Post
    # шаблон, в котором используется форма.
    template_name = 'board/post_edit.html'

    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def post(self, request, *args, **kwargs):
        print(f'request = {request}')
        print(f'user={request.user}')
        obj = Post(
            title=request.POST['title'],
            content=request.POST['content'],
            category=Category.objects.get(id=request.POST['category']),
            author=Author.objects.get(pk=request.user.id),
            attach=request.POST['attach'],
        )
        obj.save()
        return redirect('/')


# Добавляем представление для изменения публикации.
class PostUpdate(LoginRequiredMixin, UpdateView):
    # raise_exception = True
    # permission_required = ('board.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'board/post_edit.html'


# Представление удаляющее публикацию
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'board/post_delete.html'
    success_url = reverse_lazy('posts_list')


class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'board/response_add.html'

    success_url = '/board/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = User.objects.get(id=self.request.user.id)
        self.object.post = Post.objects.get(id=self.kwargs.get('pk'))
        self.object.save()
        return super().form_valid(form)


class ResponseDetail(LoginRequiredMixin, UpdateView):
    model = Response
    form_class = ResponseForm
    template_name = 'board/response.html'
    context_object_name = 'post'


def response_approve(request, pk):
    obj = Response.objects.get(id=pk)
    obj.accepted = True
    obj.save()
    return redirect('response_list')

# Представление удаляющее отклик
class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'board/response_delete.html'
    success_url = reverse_lazy('response_list')


class ResponsesList(LoginRequiredMixin, ListView):
    ordering = '-created'
    template_name = 'board/response_list.html'
    context_object_name = 'posts'

    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['posts_amount'] = len(context['posts'])
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Response.objects.filter(post__author__author=user)
        return queryset


class UserPosts(ListView):
    queryset = Post.objects.all()
    ordering = '-created'
    template_name = 'board/user_posts.html'
    context_object_name = 'posts'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['posts_amount'] = len(context['posts'])
        return context

    def get_queryset(self):
        user = self.kwargs.get('pk')
        queryset = Post.objects.filter(author__author=user)
        return queryset
