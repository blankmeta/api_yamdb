from turtle import title
from django.db import models

from .validators import year_validator
from ..users.models import User

CHOICES_RATE = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

LINE_SLICE = 20


class Category(models.Model):
    """Категории произведений

    Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
    Список категорий может быть расширен администратором.
    """
    name =  models.CharField(
        'Название категории',
        max_length=200
    )
    slug = models.SlugField(
        'Слаг категории',
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:LINE_SLICE]


class Genre(models.Model):
    """Жанр произведения

    Произведения делятся на жанры из числа предустановленных.
    Список жанров может быть расширен администратором.
    """
    name =  models.CharField(
        'Название жанра',
        max_length=200
    )
    slug = models.SlugField(
        'Слаг жанра',
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:LINE_SLICE]


class Title(models.Model):
    """Произведение - основной объект БД"""

    name = models.CharField(
        'Название произведения',
        max_length=300
    )
    description = models.TextField(
        'Описание произведения',
        blank=True,
        null=True
    )
    year = models.PositiveSmallIntegerField(
        'Год создания произведения',
        validators=[year_validator]
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name='Категория произведения'
    )

    class Meta:
        ordering = ('category', 'name')
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name[:LINE_SLICE]}, {str(self.year)}, {self.category}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(
            fields='author',
            name='unique_review')
        ]
        ordering = '-created'


class Rating(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='rating',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rating',
    )
    estimation = models.IntegerField(
        choices=CHOICES_RATE
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields='author',
            name='unique_rate')
        ]


class Comment(models.Model):
    rewiew = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = '-created'

