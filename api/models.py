from django.db.models import Model, ForeignKey, CASCADE, TextField, DateTimeField, IntegerField, UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Title(Model):
    pass


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
            f'Комментарий: {self.text[:15]} К отзыву: {self.title.text[:15]}'
            f' От автора: {self.author.username} Добавлен: {self.pub_date}'
        )
