from django.db.models CharField, ManyToManyField
from .validators import custom_year_validator

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
