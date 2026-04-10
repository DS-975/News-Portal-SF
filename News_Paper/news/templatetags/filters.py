from django_filters import FilterSet, CharFilter, DateFilter
from django import forms
from ..models import Post

class PostFilter(FilterSet):
    # Фильтр по названию (заголовку)
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'})
    )
    
    # Фильтр по автору
    author = CharFilter(
        field_name='author__authorUser__username',
        lookup_expr='icontains',
        label='Автор',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя автора'})
    )
    
    # Фильтр по дате (позже указанной)
    date_after = DateFilter(
        field_name='dateCreation',
        lookup_expr='gte',
        label='Позже даты',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'date_after']
