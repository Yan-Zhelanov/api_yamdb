from rest_framework.serializers import ModelSerializer, ChoiceField, EmailField, SlugRelatedField
from rest_framework.validators import ValidationError, UniqueTogetherValidator

from users.models import ROLES
from .models import User, Review, Comment

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
