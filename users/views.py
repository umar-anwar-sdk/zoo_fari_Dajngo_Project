from rest_framework import generics, status, views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, SignupSerializer, CustomTokenObtainPairSerializer
from .models import User
from .permissions import IsAdminUser

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        role = self.request.query_params.get('role', None)
        if role:
            return self.queryset.filter(role=role)
        return self.queryset

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def bulk_staff_approval(self, request):
        """Bulk approve/reject staff users. Expects: {"ids": [1,2], "action": "approve"|"reject"}"""
        ids = request.data.get('ids', [])
        action = request.data.get('action')
        if not isinstance(ids, (list, tuple)):
            return Response({'detail': 'ids must be a list of user IDs.'}, status=400)
        if action not in ['approve', 'reject']:
            return Response({'detail': "action must be 'approve' or 'reject'"}, status=400)
        users = User.objects.filter(pk__in=ids, role='staff')
        for u in users:
            if action == 'approve':
                u.is_approved_staff = True
                u.is_active = True
                u.is_staff = True
            else:
                u.is_approved_staff = False
                u.is_active = False
            u.save()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

class StaffApprovalView(views.APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk, role='staff')
            action = request.data.get('action') # 'approve' or 'reject'
            if action == 'approve':
                user.is_approved_staff = True
                user.is_active = True
                user.save()
                return Response({"message": "Staff approved successfully."})
            elif action == 'reject':
                user.is_approved_staff = False
                user.is_active = False
                user.save()
                return Response({"message": "Staff rejected/deactivated successfully."})
            else:
                 return Response({"error": "Invalid action. Use 'approve' or 'reject'."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Staff user not found."}, status=status.HTTP_404_NOT_FOUND)
