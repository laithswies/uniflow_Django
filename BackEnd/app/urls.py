from django.urls import path, re_path
from . import views
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)
urlpatterns = [
    path('cameras/', views.CameraListCreate.as_view(), name='camera-list-create'),
    path('gates/', views.GateListCreateRetrieveUpdateDestroy.as_view(), name='gate-list-create'),
    path('gates/<int:pk>/', views.GateListCreateRetrieveUpdateDestroy.as_view(), name='gate-detail'),
    path('gatecameras/', views.GateCameraListCreate.as_view(), name='gate-camera-list-create'),
    path('securityofficersgates/', views.SecurityOfficersGateListCreate.as_view(),
         name='security-officers-gate-list-create'),
    path('userroles/', views.UserRoleListCreate.as_view(), name='user-role-list-create'),
    path('users/', views.UserListCreate.as_view(), name='user-list-create'),
    re_path('login', views.login),
    re_path('signup', views.signup),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
