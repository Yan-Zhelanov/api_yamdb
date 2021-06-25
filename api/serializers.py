from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    EmailField,
    FloatField,
    ModelSerializer,
    Serializer,
    SlugRelatedField
)
from rest_framework.validators import ValidationError

from .models import Category, Comment, User, Genre, Review, Title

EMAIL_SUCCESSFULLY_SENT = 'Email sent! Please, check your inbox or spam.'
EMAIL_NOT_FOUND_ERROR = 'O-ops! E-mail not found!'
CONFIRMATION_CODE_INVALID = 'O-ops! Invalid confirmation code!'
REVIEW_EXISTS = 'O-ops! Review already exists!'
EMAIL_IS_EXISTS = 'O-ops! User with this e-mail already exists!'
SCORE_NOT_VALID = 'O-ops! Score not in range from 1 to 10!'
SCORE_RANGE = range(1, 11)


class SendEmailSerializer(Serializer):
    email = EmailField(required=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class GetTokenSerializer(Serializer):
    confirmation_code = CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'confirmation_code')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email',
            'role'
        )


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('pub_date',)

    def validate(self, attrs):
        if self.context['request'].method != 'POST':
            return attrs
        if Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id')
        ).exists():
            raise ValidationError(REVIEW_EXISTS)
        return attrs


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('pub_date',)


class CategoriesSerializer(ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category


class GenresSerializer(ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(ModelSerializer):
    rating = FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(TitleSerializer):
    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)


class TitleWriteSerializer(TitleSerializer):
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
