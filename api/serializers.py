from rest_framework.serializers import ModelSerializer, SerializerMethodField, EmailField

from .models import User


class UserSerializer(ModelSerializer):
    role = SerializerMethodField()
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
    
    def get_role(self, obj):
        return obj.get_role_display()
