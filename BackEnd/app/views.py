from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Camera, Gate, GateCamera, SecurityOfficersGate, UserRole, User, UserRoleEnum
from .serializers import CameraSerializer, GateSerializer, GateCameraSerializer, SecurityOfficersGateSerializer, \
    UserRoleSerializer, UserSerializer, LoginSerializer
from django.shortcuts import get_object_or_404
import bcrypt
from .utility.jwt_utility import generate_tokens
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


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


class SecurityOfficersGateListCreate(generics.ListCreateAPIView):
    queryset = SecurityOfficersGate.objects.all()
    serializer_class = SecurityOfficersGateSerializer


class UserRoleListCreate(generics.ListCreateAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# @permission_classes([IsAuthenticated])

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user_role = UserRole.objects.create(user_id=user.user_id, user_role=UserRoleEnum.USER.value)
        # access_token, refresh_token = generate_tokens({'user': serializer.data, 'user_role': user_role.user_role})
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'user_role': user_role.user_role,
            # 'access_token': access_token,
            # 'refresh_token': refresh_token,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def login(request):
#     user = get_object_or_404(User, username=request.data['username'])
#     if not user.check_password(request.data['password']):
#         return Response("missing user", status=status.HTTP_404_NOT_FOUND)
#     serializer = UserSerializer(user)
#     return Response({ 'user': serializer.data})

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username_or_email = serializer.validated_data['username_or_email']
        password = serializer.validated_data['password']

        user = authenticate(request, username_or_email=username_or_email,
                            password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {'username': user.username},  # Customize the user data as needed
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
