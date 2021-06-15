import secrets
import string

from django.core.mail import send_mail
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsAdmin
from .serializers import UserSerializer
from .models import User

EMAIL_CANNOT_BE_EMPTY = 'O-ops! E-mail cannot be empty!'
EMAIL_NOT_FOUND_ERROR = 'O-ops! E-mail not found!'
CONFIRMATION_CODE_CANNOT_BE_EMPTY = 'O-ops! Confirmation code cannot be empty!'
CONFIRMATION_CODE_INVALID = 'O-ops! Invalid confirmation code!'
EMAIL_SUCCESSFULLY_SENT = 'Email sent! Please, check your inbox or spam.'
EMAIL_SUBJECT = 'YamDB — Confirmation Code'
EMAIL_TEXT = ('You secret code for getting the token: {confirmation_code}\n'
              'Don\'t sent it on to anyone!')

class UserViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('username',)
    filterset_fields = ('username',)


class SendEmail(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        email = request.POST.get('email', None)
        if email is None:
            return Response({'error': EMAIL_CANNOT_BE_EMPTY}, status=HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email)
        if not user.exists():
            return Response({'error': EMAIL_NOT_FOUND_ERROR}, status=HTTP_400_BAD_REQUEST)
        alphabet = string.ascii_letters + string.digits
        confirmation_code = ''.join(secrets.choice(alphabet) for i in range(16))
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
            return Response({'error': EMAIL_CANNOT_BE_EMPTY}, status=HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email)
        if not user.exists():
            return Response({'error': EMAIL_NOT_FOUND_ERROR}, status=HTTP_400_BAD_REQUEST)
        user = user.first()
        confirmation_code = request.POST.get('confirmation_code', None)
        if confirmation_code is None:
            return Response({'error': CONFIRMATION_CODE_CANNOT_BE_EMPTY}, status=HTTP_400_BAD_REQUEST)
        if confirmation_code != user.confirmation_code:
            return Response({'error': CONFIRMATION_CODE_INVALID}, status=HTTP_400_BAD_REQUEST)
        token = AccessToken.for_user(user)
        return Response({'token': str(token)})
