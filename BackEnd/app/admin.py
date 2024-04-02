from django.contrib import admin
from .models import Camera, Gate, GateCamera, SecurityOfficer, SecurityOfficersGate, UserRole, User

admin.site.register(Camera)
admin.site.register(Gate)
admin.site.register(GateCamera)
admin.site.register(SecurityOfficer)
admin.site.register(SecurityOfficersGate)
admin.site.register(UserRole)
admin.site.register(User)
