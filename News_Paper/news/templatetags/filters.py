from django_filters import FilterSet, CharFilter, DateFilter
from django import forms
from ..models import Post

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class ProductFilter(FilterSet):

    # Фильтр по Заголовку
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок содержит',
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию'})
    )

    # Фильтр "v"
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
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = ['title']

    # Кастомные методы для правильной фильтрации дат
    def filter_start_date(self, queryset, name, value):
        return queryset.filter(dateCreation__date__gte=value)

    def filter_end_date(self, queryset, name, value):
        return queryset.filter(dateCreation__date__lte=value)