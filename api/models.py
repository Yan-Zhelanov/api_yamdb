from django import contrib, core, db

User = contrib.auth.get_user_model()


class Title(db.models.Model):
    pass


class Review(db.models.Model):
    author = db.models.ForeignKey(
        User,
        on_delete=db.models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        blank=False,
        null=False
    )
    title = db.models.ForeignKey(
        Title,
        on_delete=db.models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        blank=False,
        null=False
    )
    text = db.models.TextField(
        verbose_name='Отзыв',
        help_text='Оставьте ваш отзыв',
        max_length=250,
        blank=False,
        null=False
    )
    pub_date = db.models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    score = db.models.IntegerField(
        default=10,
        help_text='Поставьте этому произведению оценку от 1 до 10',
        validators=[
            core.validators.MaxValueValidator(10),
            core.validators.MinValueValidator(1)
        ],
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            db.models.UniqueConstraint(fields=['title', 'author'],
                                       name='reviews'),
        ]

    def __str__(self):
        return(f'Отзыв: {self.text[:15]} К произведению: {self.title.name}'
               f' От автора: {self.author.username} Создан: {self.pub_date}')


class Comment(db.models.Model):
    author = db.models.ForeignKey(
        User,
        on_delete=db.models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        blank=False,
        null=False
    )
    review = db.models.ForeignKey(
        Review,
        on_delete=db.models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        blank=False,
        null=False
    )
    text = db.models.TextField(
        verbose_name='Комментарий',
        help_text='Напишите ваш комментарий',
        max_length=250,
        blank=False,
        null=False
    )
    pub_date = db.models.DateTimeField(
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
