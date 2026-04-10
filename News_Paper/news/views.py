# Импортируем классы для представлений
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

# Импортируем модели, фильтры и формы
from .models import Post, Author
from .templatetags.filters import PostFilter
from .templatetags.forms import PostForm


class PostList(ListView):
    """Список всех новостей и статей с пагинацией"""
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'text'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        context['filterset'] = self.filterset
        return context


class SearchList(ListView):
    """Страница поиска с фильтрацией по названию, автору и дате"""
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = '-dateCreation'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    """Детальная страница поста"""
    model = Post
    template_name = 'new.html'
    context_object_name = 'text'


class PostUpdate(UpdateView):
    """Редактирование поста"""
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')


class PostDelete(DeleteView):
    """Удаление поста"""
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('news_list')


@login_required
def create_post(request, post_type):
    """Создание новости или статьи"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Проверяем, есть ли у пользователя Author
            if not hasattr(request.user, 'author'):
                author = Author.objects.create(authorUser=request.user)
            else:
                author = request.user.author

            post = form.save(commit=False)
            post.author = author
            post.categoryType = post_type
            post.save()

            if post_type == 'NW':
                messages.success(request, 'Новость успешно создана!')
            else:
                messages.success(request, 'Статья успешно создана!')
            return redirect('/news/')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = PostForm()

    template = 'post_edit_NW.html' if post_type == 'NW' else 'post_edit_AR.html'
    return render(request, template, {'form': form})