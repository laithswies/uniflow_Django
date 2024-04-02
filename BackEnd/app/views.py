from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Camera, Gate, GateCamera, SecurityOfficer, SecurityOfficersGate, UserRole
from .serializers import CameraSerializer, GateSerializer, GateCameraSerializer, SecurityOfficerSerializer, SecurityOfficersGateSerializer, UserRoleSerializer, UserSerializer
from django.shortcuts import render,get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class CameraListCreate(generics.ListCreateAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class GateListCreateRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView, generics.ListCreateAPIView):
    queryset = Gate.objects.all()
    serializer_class = GateSerializer

    def get_queryset(self):
        queryset = Gate.objects.all()
        location = self.request.query_params.get('location', None)
        status = self.request.query_params.get('status', None)
        if location is not None:
            queryset = queryset.filter(location=location)
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset

class GateCameraListCreate(generics.ListCreateAPIView):
    queryset = GateCamera.objects.all()
    serializer_class = GateCameraSerializer

class SecurityOfficerListCreate(generics.ListCreateAPIView):
    queryset = SecurityOfficer.objects.all()
    serializer_class = SecurityOfficerSerializer

class SecurityOfficersGateListCreate(generics.ListCreateAPIView):
    queryset = SecurityOfficersGate.objects.all()
    serializer_class = SecurityOfficersGateSerializer

class UserRoleListCreate(generics.ListCreateAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")
