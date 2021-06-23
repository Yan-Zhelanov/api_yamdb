from rest_framework.serializers import (ChoiceField,
                                        EmailField,
                                        FloatField,
                                        IntegerField,
                                        ModelSerializer,
                                        SlugRelatedField,
                                        Serializer,
                                        CharField)
from rest_framework.validators import ValidationError

from .models import Category, Comment, Genre, Review, Title, CustomUser, ROLES
from .validators import custom_year_validator

REVIEW_EXISTS = 'O-ops! Review already exists!'
EMAIL_IS_EXISTS = 'O-ops! E-mail already exists!'


class SendEmailSerializer(Serializer):
    email = EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('email',)


class GetTokenSerializer(Serializer):
    email = EmailField(required=True)
    confirmation_code = CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'confirmation_code')


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
