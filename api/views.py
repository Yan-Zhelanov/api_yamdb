import secrets
import string

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_400_BAD_REQUEST,
                                   HTTP_405_METHOD_NOT_ALLOWED)
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from users.models import ROLES

from .filters import TitleFilter
from .models import Category, Genre, Title, User
from .permissions import (IsAdminOrMe, IsAdminOrReadOnly,
                          IsAuthenticatedOrReadOnly,
                          IsAuthorOrModeratorOrAdminOrReadOnly)
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, ReviewSerializer,
                          TitlesSerializerGet, TitlesSerializerPost,
                          UserSerializer)

EMAIL_CANNOT_BE_EMPTY = 'O-ops! E-mail cannot be empty!'
EMAIL_NOT_FOUND_ERROR = 'O-ops! E-mail not found!'
CONFIRMATION_CODE_CANNOT_BE_EMPTY = 'O-ops! Confirmation code cannot be empty!'
CONFIRMATION_CODE_INVALID = 'O-ops! Invalid confirmation code!'
EMAIL_SUCCESSFULLY_SENT = 'Email sent! Please, check your inbox or spam.'
EMAIL_SUBJECT = 'YamDB — Confirmation Code'
EMAIL_TEXT = ('You secret code for getting the token: {confirmation_code}\n'
              'Don\'t sent it on to anyone!')


def update_serializer_role(self, serializer):
    role = self.request.POST.get('role', None)
    if role is None:
        return serializer.save()
    if role in ROLES:
        return serializer.save(role=role)
    return serializer.save()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminOrMe,)
    queryset = User.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    def get_object(self):
        username = self.kwargs['pk']
        if username == 'me':
            return self.request.user
        return get_object_or_404(User, username=username)

    def perform_create(self, serializer):
        update_serializer_role(self, serializer)

    def perform_update(self, serializer):
        update_serializer_role(self, serializer)

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('pk', None) == 'me':
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class SendEmail(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.POST.get('email', None)
        if email is None:
            return Response({'error': EMAIL_CANNOT_BE_EMPTY},
                            status=HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email)
        if not user.exists():
            return Response({'error': EMAIL_NOT_FOUND_ERROR},
                            status=HTTP_400_BAD_REQUEST)
        alphabet = string.ascii_letters + string.digits
        confirmation_code = ''.join(secrets.choice(alphabet)
                                    for i in range(16))
        send_mail(
            EMAIL_SUBJECT,
            EMAIL_TEXT.format(confirmation_code=confirmation_code),
            'support@yamdb.com',
            (email,)
        )
        user.update(confirmation_code=confirmation_code)
        return Response({'response': EMAIL_SUCCESSFULLY_SENT})


class GetToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.POST.get('email', None)
        if email is None:
            return Response({'error': EMAIL_CANNOT_BE_EMPTY},
                            status=HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email)
        if not user.exists():
            return Response({'error': EMAIL_NOT_FOUND_ERROR},
                            status=HTTP_400_BAD_REQUEST)
        user = user.first()
        confirmation_code = request.POST.get('confirmation_code', None)
        if confirmation_code is None:
            return Response({'error': CONFIRMATION_CODE_CANNOT_BE_EMPTY},
                            status=HTTP_400_BAD_REQUEST)
        if confirmation_code != user.confirmation_code:
            return Response({'error': CONFIRMATION_CODE_INVALID},
                            status=HTTP_400_BAD_REQUEST)
        token = AccessToken.for_user(user)
        return Response({'token': str(token)})


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrModeratorOrAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]

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
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrModeratorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)

    def get_review(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return get_object_or_404(title.reviews,
                                 id=self.kwargs['review_id'])

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
        rating=Avg('reviews__score')).order_by('name')
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitlesSerializerGet
        return TitlesSerializerPost
