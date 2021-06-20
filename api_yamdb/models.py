from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Review(models.Model):
    text = models.CharField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    score = models.IntegerField(
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации'
    )


class Comment(models.Model):
    text = models.CharField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации'
    )


class Categorie(models.Model):
    name = models.CharField(
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        verbose_name='Ключ ссылки'
    )


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        verbose_name='Ключ ссылки'
    )


class Title(models.Model):
    name = models.CharField(
        verbose_name='Имя'
    )
    year = models.IntegerField(
        verbose_name='Год'
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг'
    )
    description = models.CharField(
        verbose_name='Описание'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
    )
    category = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
    )
