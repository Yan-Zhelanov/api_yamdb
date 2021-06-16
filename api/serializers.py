from rest_framework.serializers import ModelSerializer, ChoiceField, EmailField, SlugRelatedField, IntegerField, FloatField
from rest_framework.validators import ValidationError, UniqueTogetherValidator
from .validators import custom_year_validator

from users.models import ROLES
from .models import User, Review, Comment, Category, Genre, Title

EMAIL_IS_EXISTS = 'O-ops! E-Mail "{email}" already exists!'
REVIEW_EXISTS = 'O-ops! Review already exists!'

class UserSerializer(ModelSerializer):
    role = ChoiceField(choices=ROLES, required=False)
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError(EMAIL_IS_EXISTS.format(email=email))
        return email


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ['title', 'pub_date']
        validators = [UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=['author', 'title'],
            message=REVIEW_EXISTS
        )]


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ['review', 'pub_date']


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


class TitlesSerializerGet(TitleSerializer):
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()


class TitlesSerializerPost(TitleSerializer):
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
    year = IntegerField(
        required=False,
        validators=(custom_year_validator,)
    )
