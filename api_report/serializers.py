from rest_framework import serializers

from SuspectedCase.models import SuspectedCase
from notification.models import CCEmails

SC_FIELD = [
    'pk',
    'reporter',
    'description',
    'date_reported',
    'attachment',
    'x',
    'y'
]


class SuspectedCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuspectedCase
        fields = SC_FIELD
        read_only_fields = ('date_reported', 'reporter')


class SuspectedCaseFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuspectedCase
        fields = SC_FIELD + ['status', ]
        read_only_fields = ('date_reported', 'reporter', 'description', 'attachment', 'x', 'y')


class SuspectedCaseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuspectedCase
        fields = SC_FIELD + ['status', ]
        read_only_fields = ('date_reported', 'reporter', 'description', 'attachment', 'status', 'x', 'y')


class CCEmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCEmails
        fields = ['email']
