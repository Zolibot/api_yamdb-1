from datetime import datetime

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models

from users.models import User


class CategoriesGenresAbstract(models.Model):
    """Абстрактная модель для жанров и категории"""

    name = models.CharField(
        'Название',
        max_length=256,
    )

    slug = models.SlugField(
        'Slug',
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$'
            )
        ],
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(CategoriesGenresAbstract):
    """Модель категории"""

    class Meta(CategoriesGenresAbstract.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'

    def __str__(self):
        return self.name


class Genre(CategoriesGenresAbstract):
    """Модель жанра"""

    class Meta(CategoriesGenresAbstract.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = 'genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения"""

    name = models.CharField(
        'Название',
        max_length=256,
        db_index=True,
    )
    year = models.IntegerField(
        'Год выпуска',
        db_index=True,
        default=None,
        validators=(MaxValueValidator(int(datetime.now().year)),),
    )
    description = models.TextField(
        'Описание',
        db_index=True,
        max_length=256,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель обзора и оценки произведения"""

    text = models.CharField(
        'Текст отзыва',
        max_length=150
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        'Оценка',
        default=1,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={
            'validators': 'Оценка от 1 до 10!'
        }
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_autor'
            )
        ]

    def __str__(self):
        return f'Обзор {self.author} на {self.title}'


class Comment(models.Model):
    """Модель комментария к произведению"""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Пользователь'
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField()
