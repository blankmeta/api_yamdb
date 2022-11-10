from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User
from .validators import year_validator

LINE_SLICE = 20


class Category(models.Model):
    """Категории произведений

    Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
    Список категорий может быть расширен администратором.
    """
    name = models.CharField(
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
    name = models.CharField(
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
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='genre',
        verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
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
        related_name='reviews',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['author', 'title'],
            name='unique_review')
        ]
        ordering = ('-pub_date',)


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
