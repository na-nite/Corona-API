from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, generics, exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from SuspectedCase.models import SuspectedCase
from notification.models import CCEmails
from .serializers import SuspectedCaseSerializer, SuspectedCaseFullSerializer, CCEmailsSerializer

from app.settings import EMAIL_HOST

from .serializers import SuspectedCaseStatusSerializer


class ReportCase(generics.CreateAPIView, ):
    """
    report a case
    """
    serializer_class = SuspectedCaseSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if self.request.user.role == 1:
            return SuspectedCase.objects.all()
        else:
            raise exceptions.PermissionDenied()

    def perform_create(self, serializer):
        if self.request.user.role == 1:
            serializer.save(reporter=self.request.user)
        else:
            raise exceptions.PermissionDenied()


class ListCases(generics.ListAPIView):
    """
    list reported cases
    """
    serializer_class = SuspectedCaseFullSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'reporter', 'date_reported']
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if self.request.user.role == 2:
            return SuspectedCase.objects.all()
        else:
            raise exceptions.PermissionDenied()


class AcceptCases(generics.RetrieveUpdateAPIView):
    """
    accept a reported case
    """
    serializer_class = SuspectedCaseStatusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'reporter', 'date_reported']
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if self.request.user.role == 2:
            return SuspectedCase.objects.all()
        else:
            raise exceptions.PermissionDenied()

    def perform_update(self, serializer):
        serializer.save(status=2)
        cc = CCEmails.objects.all()
        for c in cc:
            send_mail("[Corona-Watch] Nouveau cas signalé",
                      "",
                      EMAIL_HOST,
                      [c.email],
                      fail_silently=False)


class RejectCases(generics.RetrieveUpdateAPIView):
    """
    reject a reported case
    """
    serializer_class = SuspectedCaseStatusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'reporter', 'date_reported']
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if self.request.user.role == 2:
            return SuspectedCase.objects.all()
        else:
            raise exceptions.PermissionDenied()

    def perform_update(self, serializer):
        serializer.save(status=3)


class AddEmails(generics.CreateAPIView):
    serializer_class = CCEmailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 4 or self.request.user.role == 2:
            return CCEmails.objects.all()
        else:
            raise exceptions.PermissionDenied()


class CCEmailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CCEmailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 4 or self.request.user.role == 2:
            return CCEmails.objects.all()
        else:
            raise exceptions.PermissionDenied()

