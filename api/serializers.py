from rest_framework import serializers, validators

from .models import Comment, Review

REVIEW_EXISTS = 'Вы уже писли отзыв на это произведение.'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ['title', 'pub_date']
        validators = [validators.UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=['author', 'title'],
            message=REVIEW_EXISTS
        )]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ['review', 'pub_date']
