from rest_framework import serializers
from .models import BacktestJob


class BacktestJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = BacktestJob
        fields = '__all__'
