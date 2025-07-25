# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from .models import Post
from .templatetags.filters import ProductFilter

from datetime import datetime


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'  # Сортировка по убыванию даты
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'text'
    paginate_by = 5  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш клас фильтрации
        # self.request.GET содержит объект QueryDict.
        # Сохраняем нашу фильтрацию в области класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ProductFilter(self.request.GET, queryset)
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)

        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.now()

        # # Добавим ещё одну пустую переменную,
        # # чтобы на её примере рассмотреть работу ещё одного фильтра.
        # context['filterset'] = self.filterset
        # context['text'] = self.news_list

        context['filterset'] = self.filterset

        # Вывод всего словаря context
        # pprint(context)
        return context


# Вот так мы можем использовать дженерик ListView для вывода списка товаров:
#
# Создаем свой класс, который наследуется от ListView.
# Указываем модель, из которой будем выводить данные.
# Указываем поле сортировки данных модели (необязательно).
# Записываем название шаблона.
# Объявляем, как хотим назвать переменную в шаблоне.

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — new.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'text'



