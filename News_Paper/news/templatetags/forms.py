from django import forms
from django.core.exceptions import ValidationError

from ..models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'categoryType',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите уникальный заголовок'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите уникальный текст новости'
            }),
            'categoryType': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок',
            'text': 'Текст новости',
            'categoryType': 'Тип публикации',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')

        # Проверяем, существует ли пост с таким заголовком
        if Post.objects.filter(title__iexact=title).exists():  # Без учета регистра
            raise ValidationError('Новость с таким заголовком уже существует!')

        # Дополнительные проверки заголовка
        if len(title) < 5:
            raise ValidationError('Заголовок слишком короткий! Минимум 5 символов.')

        if len(title) > 128:
            raise ValidationError('Заголовок слишком длинный! Максимум 128 символов.')

        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')

        # Проверяем, существует ли пост с таким текстом
        if Post.objects.filter(text__iexact=text).exists():  # Без учета регистра
            raise ValidationError('Новость с таким текстом уже существует!')

        # Дополнительные проверки текста
        if len(text) < 20:
            raise ValidationError('Текст слишком короткий! Минимум 20 символов.')

        return text

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        # Дополнительная проверка: если и заголовок, и текст совпадают
        if title and text:
            if Post.objects.filter(title__iexact=title, text__iexact=text).exists():
                raise ValidationError('Такая новость (с таким заголовком и текстом) уже существует!')

        return cleaned_data