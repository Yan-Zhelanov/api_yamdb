from rest_framework.serializers import (CharField,
                                        ChoiceField,
                                        CurrentUserDefault,
                                        EmailField,
                                        FloatField,
                                        ModelSerializer,
                                        Serializer,
                                        SlugRelatedField)
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from .models import ROLES, Category, Comment, CustomUser, Genre, Review, Title

EMAIL_SUCCESSFULLY_SENT = 'Email sent! Please, check your inbox or spam.'
EMAIL_NOT_FOUND_ERROR = 'O-ops! E-mail not found!'
CONFIRMATION_CODE_INVALID = 'O-ops! Invalid confirmation code!'
REVIEW_EXISTS = 'O-ops! Review already exists!'
EMAIL_IS_EXISTS = 'O-ops! E-mail already exists!'

EMAIL_IS_EXISTS = 'O-ops! E-Mail "{email}" already exists!'
REVIEW_EXISTS = 'O-ops! Review already exists!'
SCORE_NOT_VALID = 'O-ops! Score not in range from 1 to 10!'
SCORE_RANGE = range(1, 11)


class GetTokenSerializer(Serializer):
    email = EmailField(required=True)
    confirmation_code = CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'confirmation_code')

    def validate(self, attrs):
        user = CustomUser.objects.filter(email=attrs.get('email'))
        if not user.exists():
            raise ValidationError({'error': EMAIL_NOT_FOUND_ERROR})
        if user.first().confirmation_code != attrs.get('confirmation_code'):
            raise ValidationError({'error': CONFIRMATION_CODE_INVALID})
        return {'token': str(AccessToken.for_user(user.first()))}


class UserSerializer(ModelSerializer):
    role = ChoiceField(choices=ROLES, required=False)
    email = EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email',
            'role'
        )

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(EMAIL_IS_EXISTS.format(email=email))
        return email


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ['title', 'pub_date']

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
        fields = '__all__'
        model = Comment
        read_only_fields = ('review', 'pub_date')


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
