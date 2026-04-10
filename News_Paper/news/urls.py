from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, create_post, SearchList, PostUpdate, PostDelete

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name='news_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>/', PostDetail.as_view(), name='news_detail'),
   path('create_nw/', create_post, {'post_type': 'NW'}, name='post_create_nw'),
   path('create_ar/', create_post, {'post_type': 'AR'}, name='post_create_ar'),

   # Новая страница поиска
   path('search/', SearchList.as_view(), name='search'),

   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]