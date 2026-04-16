from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')), # для стилей
    path('news/', include('news.urls')), # все URL приложения news
    path('new/', include('news.urls')),

    # ===== СТРАНИЦЫ АУНТИФИКАЦИИ ===== 
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
