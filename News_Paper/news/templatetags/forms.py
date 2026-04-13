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
        instance = self.instance  # Получаем текущий редактируемый объект

        # Проверяем, существует ли пост с таким заголовком, ИСКЛЮЧАЯ текущий
        if instance and instance.pk:
            # Режим редактирования - исключаем текущий пост из проверки
            if Post.objects.filter(title__iexact=title).exclude(pk=instance.pk).exists():
                raise ValidationError('Новость с таким заголовком уже существует!')
        else:
            # Режим создания - проверяем все посты
            if Post.objects.filter(title__iexact=title).exists():
                raise ValidationError('Новость с таким заголовком уже существует!')

        if len(title) < 5:
            raise ValidationError('Заголовок слишком короткий! Минимум 5 символов.')

        if len(title) > 128:
            raise ValidationError('Заголовок слишком длинный! Максимум 128 символов.')

        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        instance = self.instance

        # Проверяем, существует ли пост с таким текстом, ИСКЛЮЧАЯ текущий
        if instance and instance.pk:
            if Post.objects.filter(text__iexact=text).exclude(pk=instance.pk).exists():
                raise ValidationError('Новость с таким текстом уже существует!')
        else:
            if Post.objects.filter(text__iexact=text).exists():
                raise ValidationError('Новость с таким текстом уже существует!')

        if len(text) < 20:
            raise ValidationError('Текст слишком короткий! Минимум 20 символов.')

        return text

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        instance = self.instance

        if title and text:
            if instance and instance.pk:
                if Post.objects.filter(title__iexact=title, text__iexact=text).exclude(pk=instance.pk).exists():
                    raise ValidationError('Такая новость (с таким заголовком и текстом) уже существует!')
            else:
                if Post.objects.filter(title__iexact=title, text__iexact=text).exists():
                    raise ValidationError('Такая новость (с таким заголовком и текстом) уже существует!')

        return cleaned_data