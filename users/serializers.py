from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'password',
                  )

class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        '''Токен для авторизации и регистрации'''
        token = super().get_token(user)
        token['email'] = user.email
        if hasattr(user, 'tg_id'):
            token['tg_id'] = user.tg_id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'email': self.user.email,
            'id': self.user.id
        })
        return data