from diagnostic.models import Diagnose
from rest_framework.fields import SerializerMethodField
from rest_framework import serializers


diagnose_FIELDS = [
    'pk',
    'temperature',
    'pace',
    'weight',
    'age',
    'user',]

answer_fleids = [
    'pk',
    'temperature',
    'pace',
    'weight',
    'age',
    'user',
    'answer',
]

class DiagnoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnose
        fields = diagnose_FIELDS
        read_only_fields = ('answer',)

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnose
        fields = answer_fleids
        read_only_fields = ('pk','temperature','pace','weight','age', 'user', 'answer',)


