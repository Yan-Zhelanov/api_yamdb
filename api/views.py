import string

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import (SAFE_METHODS,
                                        AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import ROLES

from .filters import TitleFilter
from .models import Category, Genre, Review, Title, CustomUser
from .permissions import (IsAdmin,
                          IsAdminOrReadOnly,
                          IsAuthorOrModeratorOrAdminOrReadOnly,)
from .serializers import (CategoriesSerializer,
                          CommentSerializer,
                          GenresSerializer,
                          ReviewSerializer,
                          TitlesSerializerGet,
                          TitlesSerializerPost,
                          UserSerializer,
                          GetTokenSerializer,
                          EMAIL_NOT_FOUND_ERROR,
                          EMAIL_SUCCESSFULLY_SENT)

EMAIL_CANNOT_BE_EMPTY = 'O-ops! E-mail cannot be empty!'
CONFIRMATION_CODE_CANNOT_BE_EMPTY = 'O-ops! Confirmation code cannot be empty!'
EMAIL_SUBJECT = 'YamDB - Confirmation Code'
EMAIL_TEXT = ('You secret code for getting the token: {confirmation_code}\n'
              'Don\'t sent it on to anyone!')
KEY_FOR_MY_PROFILE = 'me'
CONFIRMATION_CODE_LENGTH = 16


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    queryset = CustomUser.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=('GET', 'PATCH',), detail=False, permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
        else:
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        return Response(serializer.data)

    def update_serializer_role(self, serializer):
        role = self.request.data.get('role')
        if role is None:
            return serializer.save()
        for expected_role, _ in ROLES:
            if role == expected_role:
                return serializer.save(role=role)
        return serializer.save()

    def perform_create(self, serializer):
        self.update_serializer_role(serializer)

    def perform_update(self, serializer):
        self.update_serializer_role(serializer)


class SendEmail(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if email is None:
            return Response(
                {'error': EMAIL_CANNOT_BE_EMPTY},
                status=HTTP_400_BAD_REQUEST
            )
        user = CustomUser.objects.filter(email=email)
        if not user.exists():
            return Response(
                {'error': EMAIL_NOT_FOUND_ERROR},
                status=HTTP_400_BAD_REQUEST
            )
        alphabet = string.ascii_letters + string.digits
        confirmation_code = get_random_string(CONFIRMATION_CODE_LENGTH, alphabet)
        send_mail(
            EMAIL_SUBJECT,
            EMAIL_TEXT.format(confirmation_code=confirmation_code),
            'support@yamdb.com',
            (email,)
        )
        user.update(confirmation_code=confirmation_code)
        return Response({'response': EMAIL_SUCCESSFULLY_SENT})


class GetToken(TokenViewBase):
    permission_classes = (AllowAny,)
    serializer_class = GetTokenSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )

    def perform_update(self, serializer):
        serializer.save()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend,)

    def get_review(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return get_object_or_404(
            title.reviews, id=self.kwargs['review_id']
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class CreateDelListViewset(CreateModelMixin, DestroyModelMixin,
                           ListModelMixin, GenericViewSet):
    pass


class CategoriesViewSet(CreateDelListViewset):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(CreateDelListViewset):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitlesViewset(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer
