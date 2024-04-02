from rest_framework import serializers
from .models import Camera, Gate, GateCamera, SecurityOfficer, SecurityOfficersGate, UserRole
from django.contrib.auth.models import User
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

class SecurityOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityOfficer
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
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']
