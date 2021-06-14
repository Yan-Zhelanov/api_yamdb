import secrets
import string

from django.core.mail import send_mail
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions import IsAdmin
from .serializers import UserSerializer
from .models import User


class UserViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin):
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('username',)


class SendEmail(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        email = request.POST.get('email', None)
        user = User.objects.filter(email=email)
        if not user.exists():
            return Response({'error': 'E-mail not found'})
        alphabet = string.ascii_letters + string.digits
        code_confirmation = ''.join(secrets.choice(alphabet) for i in range(16))
        send_mail(
            'YamDB — Code Confirmation',
            (f'You secret code for getting the token: {code_confirmation}\n'
             'Don\'t sent it on to anyone!'),
             'support@yamdb.com',
            (email,)
        )
        user.code_confirmation = code_confirmation
        return Response({'response': 'Email sent! Please, check your inbox or spam.'})

