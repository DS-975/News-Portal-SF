from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from django import forms
from ..models import Post, Title, PostTitle

class ProductFilter(FilterSet):
    # Фильтр по текстовому поиску
    title_search = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Поиск по заголовку',
        widget=forms.TextInput(attrs={'placeholder': 'Введите часть заголовка'})
    )

    # Фильтр по выбору из списка заголовков (теперь по связи с Title)
    title_list = ModelChoiceFilter(
        field_name='title',  # Фильтруем по названию связанного заголовка
        queryset=Post.objects.all(),
        label='Выберите из списка заголовков',
        empty_label='Все заголовки'
    )

    # Фильтр "От даты"
    start_date = DateFilter(
        field_name='dateCreation',
        lookup_expr='gte',
        label='От даты',
        widget=forms.DateInput(attrs={'type': 'date'}),
        method='filter_start_date'
    )

    # Фильтр "До даты"
    end_date = DateFilter(
        field_name='dateCreation',
        lookup_expr='lte',
        label='До даты',
        widget=forms.DateInput(attrs={'type': 'date'}),
        method='filter_end_date'
    )



    class Meta:
        model = Post
        fields = []  # Оставляем пустым, так как все фильтры объявлены явно

    def filter_start_date(self, queryset, name, value):
        return queryset.filter(dateCreation__date__gte=value)

    def filter_end_date(self, queryset, name, value):
        return queryset.filter(dateCreation__date__lte=value)