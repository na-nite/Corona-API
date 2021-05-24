from rest_framework import serializers

from zone.models import NationalZone, InternationalZone
from zone_store.models import Wilaya, Commune

ZONE_FIELDS_USER = ['pk',
                    'x',
                    'y',
                    'name',
                    'dead',
                    'sick',
                    'recovered',
                    'infected']

ZONE_FIELDS_STAFF = ZONE_FIELDS_USER + ['status']

ZONE_READ_ONLY = ('x', 'y', 'name', 'dead', 'sick', 'recovered', 'infected')


class NationalZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalZone
        fields = ZONE_FIELDS_USER + ['is_risky', 'remarque']
        read_only_fields = ZONE_READ_ONLY + ('is_risky', 'remarque', 'status')


class FullNationalZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalZone
        fields = ZONE_FIELDS_STAFF + ['is_risky', 'remarque']
        read_only_fields = ('status',)


class NationalZoneStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalZone
        fields = ZONE_FIELDS_STAFF + ['is_risky', 'remarque']
        read_only_fields = ZONE_READ_ONLY + ('is_risky', 'remarque')


class InternationalZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternationalZone
        fields = ZONE_FIELDS_USER + ['continent', 'carrier']
        read_only_fields = ZONE_READ_ONLY + ('continent', 'carrier')


class FullInternationalZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternationalZone
        fields = ZONE_FIELDS_STAFF + ['continent', 'carrier']
        read_only_fields = ('status',)


class InternationalZoneStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternationalZone
        fields = ZONE_FIELDS_STAFF + ['continent', 'carrier']
        read_only_fields = ZONE_READ_ONLY + ('continent', 'carrier')


class WilayaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wilaya
        fields = ['pk', 'code', 'nom']
        read_only_fields = ('pk', 'code', 'nom')


class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = ['pk', 'wilaya', 'latitude', 'longitude', 'nom']
        read_only_fields = ('latitude', 'longitude', 'nom', 'wilaya', 'pk')
