import hashlib
import hmac

from rest_framework import serializers
from .models import Camera, Gate, GateCamera, SecurityOfficersGate, UserRole, User, UserRoleEnum
import bcrypt

from .secret import SECRET_KEY


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'


class GateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gate
        fields = '__all__'


class GateCameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = GateCamera
        fields = '__all__'


class SecurityOfficersGateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityOfficersGate
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'username', 'is_account_verified']

    def create(self, validated_data):
        password = validated_data.pop('password')
        h = hmac.new(SECRET_KEY.encode(), digestmod=hashlib.sha256)
        h.update(password.encode())
        validated_data['password_hash'] = h.hexdigest()
        data = super(UserSerializer, self).create(validated_data)
        return data
    
class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        if not username_or_email or not password:
            raise serializers.ValidationError('Username or email and password are required.')

        return data
