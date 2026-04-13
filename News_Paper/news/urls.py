from django.urls import path
from .views import (
    PostList, PostDetail, create_post, SearchList,
    NewsCreate, NewsUpdate, NewsDelete,
    ArticleCreate, ArticleUpdate, ArticleDelete
)

urlpatterns = [
    # Основные страницы
    path('', PostList.as_view(), name='news_list'),
    path('search/', SearchList.as_view(), name='search'),
    path('<int:pk>/', PostDetail.as_view(), name='news_detail'),
    
    # Создание (через функцию - старый способ)
    path('create_nw/', create_post, {'post_type': 'NW'}, name='post_create_nw'),
    path('create_ar/', create_post, {'post_type': 'AR'}, name='post_create_ar'),
    
    # CRUD для НОВОСТЕЙ (через классы)
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    
    # CRUD для СТАТЕЙ (через классы)
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]