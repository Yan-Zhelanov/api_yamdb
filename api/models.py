from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (CASCADE, DO_NOTHING, CharField, DateTimeField,
                              ForeignKey, IntegerField, ManyToManyField, Model,
                              SlugField, TextField, UniqueConstraint)

from .validators import custom_year_validator

User = get_user_model()


class Category(Model):
    name = CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='Название'
    )
    slug = SlugField(
        max_length=40,
        unique=True,
        verbose_name='Метка'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(Model):
    name = CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='Название'
    )
    slug = SlugField(
        max_length=40,
        unique=True,
        verbose_name='Метка'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(Model):
    name = CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='Название'
    )
    year = IntegerField(
        null=True,
        verbose_name='Год',
        validators=[
            custom_year_validator
        ]
    )
    description = TextField(
        null=True,
        verbose_name='Описание'
    )
    category = ForeignKey(
        Category,
        on_delete=DO_NOTHING,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(Model):
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        blank=False,
        null=False
    )
    title = ForeignKey(
        Title,
        on_delete=CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        blank=False,
        null=False
    )
    text = TextField(
        verbose_name='Отзыв',
        help_text='Оставьте ваш отзыв',
        max_length=250,
        blank=False,
        null=False
    )
    pub_date = DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    score = IntegerField(
        default=10,
        help_text='Поставьте этому произведению оценку от 1 до 10',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            UniqueConstraint(fields=['title', 'author'],
                             name='reviews'),
        ]

    def __str__(self):
        return(f'Отзыв: {self.text[:15]} К произведению: {self.title.name}'
               f' От автора: {self.author.username} Создан: {self.pub_date}')


class Comment(Model):
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='comments',
        verbose_name='Автор',
        blank=False,
        null=False
    )
    review = ForeignKey(
        Review,
        on_delete=CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        blank=False,
        null=False
    )
    text = TextField(
        verbose_name='Комментарий',
        help_text='Напишите ваш комментарий',
        max_length=250,
        blank=False,
        null=False
    )
    pub_date = DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return(
            f'Комментарий: {self.text[:15]} К отзыву: {self.review.text[:15]}'
            f' От автора: {self.author.username} Добавлен: {self.pub_date}'
        )
