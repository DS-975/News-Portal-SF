# Импортируем классы для представлений
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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







    # ========== CRUD ДЛЯ НОВОСТЕЙ ==========
class NewsCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit_NW.html'
    success_url = reverse_lazy('news_list')
    login_url = '/accounts/login/' # перенапраление для неавторизованных
    
    def form_valid(self, form):
        form.instance.categoryType = 'NW'
        return super().form_valid(form)

class NewsUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit_NW.html'
    success_url = reverse_lazy('news_list')
    login_url = '/accounts/login/' # перенапраление для неавторизованных
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Новость успешно обновлена!')
        return response

class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('news_list')
    login_url = '/accounts/login/' # перенапраление для неавторизованных

# ========== CRUD ДЛЯ СТАТЕЙ ==========
class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit_AR.html'
    success_url = reverse_lazy('news_list')
    login_url = '/accounts/login/' # перенапраление для неавторизованных
    
    def form_valid(self, form):
        form.instance.categoryType = 'AR'
        return super().form_valid(form)

class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit_AR.html'
    success_url = reverse_lazy('news_list')
    login_url = '/accounts/login/' # перенапраление для неавторизованных

class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('news_list')
    login_url = '/accounts/login/' # перенапраление для неавторизованных






# ========== АУТИФИКАЦИЯ ==========

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'prodected_page.html'
    login_url = '/accounts/login' # перенаправление для неавторизованных
    redirect_field_name = 'next' # параметер для возврата после входа

