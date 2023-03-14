from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class User(models.Model):
    """Заглушка"""

    username = models.CharField(max_length=256)
    email = models.EmailField()
    role = models.CharField(max_length=256)
    bio = models.CharField(max_length=500)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)


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
        ordering = ('name', )

    def __str__(self):
        return self.name


class Category(CategoriesGenresAbstract):
    """Модель категории"""

    class Meta(CategoriesGenresAbstract.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'


class Genre(CategoriesGenresAbstract):
    """Модель жанра"""

    class Meta(CategoriesGenresAbstract.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = 'genres'


class Titles(models.Model):
    """Модель произведения"""

    name = models.CharField(
        'Название',
        max_length=256,
        db_index=True,
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        db_index=True,
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
        through='Genre_Title',
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Genre_Title(models.Model):
    """Вспомогательная модель многие к многим"""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель обзора и оценки произведения"""

    text = models.CharField(
        'Текст отзыва',
        max_length=6000
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )

    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
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
            # models.UniqueConstraint(
            #     fields=['author', 'title'],
            #     name='unique_autor'
            # )
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
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField()

    def __str__(self):
        return self.author
