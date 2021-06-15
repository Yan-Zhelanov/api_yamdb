from rest_framework.serializers import ModelSerializer, ChoiceField, EmailField, SerializerMethodField
from rest_framework.validators import ValidationError

from users.models import ROLES
from .models import User

EMAIL_IS_EXISTS = 'O-ops! E-Mail "{email}" already exists!'

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
