from django.urls import path,re_path
from . import views

urlpatterns = [
    path('cameras/', views.CameraListCreate.as_view(), name='camera-list-create'),
    path('gates/', views.GateListCreateRetrieveUpdateDestroy.as_view(), name='gate-list-create'),
    path('gates/<int:pk>/', views.GateListCreateRetrieveUpdateDestroy.as_view(), name='gate-detail'),
    path('gatecameras/', views.GateCameraListCreate.as_view(), name='gate-camera-list-create'),
    path('securityofficers/', views.SecurityOfficerListCreate.as_view(), name='security-officer-list-create'),
    path('securityofficersgates/', views.SecurityOfficersGateListCreate.as_view(), name='security-officers-gate-list-create'),
    path('userroles/', views.UserRoleListCreate.as_view(), name='user-role-list-create'),
    path('users/', views.UserListCreate.as_view(), name='user-list-create'),
    re_path('login',views.login),
    re_path('signup',views.signup),
    re_path('test_token', views.test_token)
]