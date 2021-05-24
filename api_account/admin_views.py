from user.models import User
from .serializers import UserSerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend


class UserList(generics.ListAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        filter_backends = [DjangoFilterBackend]
        filterset_fields = ['is_staff', 'is_active','role']
