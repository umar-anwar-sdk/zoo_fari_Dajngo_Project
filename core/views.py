from rest_framework import viewsets, permissions
from .models import Category, Animal, FamilyPackage
from .serializers import CategorySerializer, AnimalSerializer, FamilyPackageSerializer
from users.permissions import IsStaffOrAdminUser

class IsStaffAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.role in ['admin', 'staff'])

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsStaffAdminOrReadOnly,)

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (IsStaffAdminOrReadOnly,)

class FamilyPackageViewSet(viewsets.ModelViewSet):
    queryset = FamilyPackage.objects.all()
    serializer_class = FamilyPackageSerializer
    permission_classes = (IsStaffAdminOrReadOnly,)
