from enum import Enum

from django.contrib.auth.models import User
from django.db import models


class Camera(models.Model):
    class Meta:
        db_table = 'camera'
        managed = False
    camera_id = models.AutoField(primary_key=True)
    resolution = models.CharField(max_length=30)
    trained_model = models.CharField(max_length=10, choices=[(tag, tag) for tag in ['YOLO', 'RCNN', 'SSD']])
    fps = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Gate(models.Model):
    class Meta:
        db_table = 'gates'
        managed = False

    gate_id = models.AutoField(primary_key=True)
    location = models.TextField()
    status = models.CharField(max_length=10, choices=[(tag, tag) for tag in ['CLOSED', 'OPEN']])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GateCamera(models.Model):
    class Meta:
        db_table = 'gates_cameras'
        managed = False

    gate_camera_id = models.AutoField(primary_key=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SecurityOfficersGate(models.Model):
    class Meta:
        db_table = 'security_officers_gate'
        managed = False

    security_officers_gate_id = models.AutoField(primary_key=True)
    security_officer = models.ForeignKey(User, on_delete=models.CASCADE)
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE)
    work_shift = models.CharField(max_length=5, choices=[(tag, tag) for tag in ['DAY', 'NIGHT']])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserRole(models.Model):
    class Meta:
        db_table = 'users_roles'
        managed = False

    user_role_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[(tag, tag) for tag in ['USER', 'ADMIN', 'SECURITY_OFFICER']])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    class Meta:
        db_table = 'users'
        managed = False

    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserRoleEnum(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    SECURITY_OFFICER = 'SECURITY_OFFICER'
