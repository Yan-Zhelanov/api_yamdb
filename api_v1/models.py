from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=40,
        unique=True,
        verbose_name='Метка'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=40,
        unique=True,
        verbose_name='Метка'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='Название'
    )
    year = models.IntegerField(
        null=True,
        verbose_name='Год',
        validators=[
            custom_year_validator
        ]
    )
    description = models.TextField(
        null=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='title',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='title',
        verbose_name='Жанр'
    )
