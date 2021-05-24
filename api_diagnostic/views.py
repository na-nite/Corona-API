from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api_diagnostic.serializers import DiagnoseSerializer, AnswerSerializer
from diagnostic.models import Diagnose


class DiagnoseCreate(generics.CreateAPIView):
    serializer_class = DiagnoseSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = Diagnose.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role == 1:
            serializer.save(user=self.request.user)
        else:
            raise exceptions.ValidationError("this user is not allowed to create posts")


class Answer(generics.RetrieveAPIView):
    serializer_class = AnswerSerializer
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        return AnswerSerializer

    def get_queryset(self):
        return Diagnose.objects.all().filter(user=self.request.user)
