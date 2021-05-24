from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, generics, exceptions
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api_map.serializers import NationalZoneSerializer, FullNationalZoneSerializer, NationalZoneStatusSerializer, \
    InternationalZoneStatusSerializer, InternationalZoneSerializer, FullInternationalZoneSerializer, WilayaSerializer, \
    CommuneSerializer
from zone.models import NationalZone, InternationalZone
from zone_store.models import Wilaya, Commune

FILTER_FIELDS = ['is_risky', 'name']


class NationalZoneList(mixins.CreateModelMixin, generics.ListAPIView, ):
    """
    retrieve national zone lists
    """
    serializer_class = NationalZoneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = FILTER_FIELDS
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 4 or self.request.user.is_superuser:
                return FullNationalZoneSerializer
        return NationalZoneSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            qs = NationalZone.objects.all()
        else:
            qs = NationalZone.objects.all().filter(status='a')
        return qs


class NationalZoneListId(generics.RetrieveAPIView):
    """
    list  National Zone by Id
    """
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = FILTER_FIELDS
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 4 or self.request.user.is_superuser:
                return FullNationalZoneSerializer
        return NationalZoneSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            qs = NationalZone.objects.all()
        else:
            qs = NationalZone.objects.all().filter(status='a')
        return qs


class NationalZoneCreate(generics.CreateAPIView):
    """
    Create  National Zones
    """
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 4 or self.request.user.is_superuser:
                return FullNationalZoneSerializer
        return NationalZoneSerializer

    def get_queryset(self):
        if self.request.user.role == 4:
            return NationalZone.objects.all()
        else:
            raise exceptions.ValidationError("this user is not allowed to create zones")

    def perform_create(self, serializer):
        if self.request.user.role == 4:
            serializer.save()
        else:
            raise exceptions.ValidationError("this user is not allowed to create zones")


class NationalZoneRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """
    Update National Zone
    """
    queryset = NationalZone.objects.all()
    serializer_class = FullNationalZoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 4 or self.request.user.is_superuser:
            qs = NationalZone.objects.all().filter()
            return qs
        else:
            raise exceptions.ValidationError("this user is not allowed to update zone")

    def perform_update(self, serializer):
        if self.request.user.role == 4 or self.request.user.is_superuser:
            serializer.save(status='p')
        else:
            raise exceptions.ValidationError("this user is not allowed to update zone")


class NationalZoneStatusUpdate(generics.RetrieveUpdateAPIView):
    """
    moderator can approve a national zone added or updated
    """
    queryset = NationalZone.objects.all()
    serializer_class = NationalZoneStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 2 or self.request.user.is_superuser:
            qs = NationalZone.objects.all().filter()
            return qs
        else:
            raise exceptions.ValidationError("this user is not allowed to change the status of the update")

    def get_serializer_class(self):
        if self.request.user.role == 2 or self.request.user.is_superuser:
            return NationalZoneStatusSerializer
        return NationalZoneSerializer


""" INTERNATIONAL ZONES """
FILTER_FIELDS_INTER = ['continent', 'name', ]


class InternationalZoneList(mixins.CreateModelMixin, generics.ListAPIView, ):
    """
    retrieve International Zone lists
    """
    serializer_class = InternationalZoneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = FILTER_FIELDS_INTER
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 4 or self.request.user.is_superuser:
                return FullInternationalZoneSerializer
        return InternationalZoneSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            qs = InternationalZone.objects.all()
        else:
            qs = InternationalZone.objects.all().filter(status='a')
        return qs


class InternationalZoneListId(generics.RetrieveAPIView):
    """
    list  International Zone by Id
    """
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = FILTER_FIELDS_INTER
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 4 or self.request.user.is_superuser:
                return FullInternationalZoneSerializer
        return InternationalZoneSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            qs = InternationalZone.objects.all()
        else:
            qs = InternationalZone.objects.all().filter(status='a')
        return qs


class InternationalZoneCreate(generics.CreateAPIView):
    """
    Create  International Zones
    """
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 4 or self.request.user.is_superuser:
                return FullInternationalZoneSerializer
        return InternationalZoneSerializer

    def get_queryset(self):
        if self.request.user.role == 4 or self.request.user.is_superuser:
            return InternationalZone.objects.all()
        else:
            raise exceptions.ValidationError("this user is not allowed to create zones")

    def perform_create(self, serializer):
        if self.request.user.role == 4 or self.request.user.is_superuser:
            serializer.save()
        else:
            raise exceptions.ValidationError("this user is not allowed to create zones")


class InternationalZoneRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """
    Update International Zone
    """
    queryset = InternationalZone.objects.all()
    serializer_class = FullInternationalZoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 4 or self.request.user.is_superuser:
            qs = InternationalZone.objects.all().filter()
            return qs
        else:
            raise exceptions.ValidationError("this user is not allowed to update zone")

    def perform_update(self, serializer):
        if self.request.user.role == 4 or self.request.user.is_superuser:
            serializer.save(status='p')
        else:
            raise exceptions.ValidationError("this user is not allowed to update zone")


class InternationalZoneStatusUpdate(generics.RetrieveUpdateAPIView):
    """
    moderator can approve a International Zone added or updated
    """
    queryset = InternationalZone.objects.all()
    serializer_class = InternationalZoneStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 2 or self.request.user.is_superuser:
            qs = InternationalZone.objects.all().filter()
            return qs
        else:
            raise exceptions.ValidationError("this user is not allowed to change the status of the update")

    def get_serializer_class(self):
        if self.request.user.role == 2 or self.request.user.is_superuser:
            return InternationalZoneStatusSerializer
        return InternationalZoneSerializer

    """ WILAYA & COMMUNES """


class Wilayas(generics.ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = WilayaSerializer
    queryset = Wilaya.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['code', 'nom']


class Communes(generics.ListAPIView, generics.RetrieveAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = CommuneSerializer
    queryset = Commune.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['wilaya', 'nom']
