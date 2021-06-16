from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Review, Comment, Genre, Category, Title


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('title', 'text', 'author',)
    search_fields = ('title', 'author',)
    empty_value_display = '<empty>'


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('review', 'text', 'author',)


@admin.register(Title)
class TitleAdmin(ModelAdmin):
    list_display = ('name', 'year', 'description', 'category',)
    search_fields = ('name',)
    list_filter = ('category',)
    empty_value_display = '<empty>'


@admin.register(Genre)
class GenreAdmin(ModelAdmin):
    list_display = ('name', 'slug',)
    empty_value_display = '<empty>'


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug',)
    empty_value_display = '<empty>'
