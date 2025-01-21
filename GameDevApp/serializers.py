from rest_framework import serializers
from .models import Vacancy, CustomUser, Main, DemandChart, GeoChart, Skills, Statistic

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'is_admin')

class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Main
        fields = '__all__'

class DemandChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandChart
        fields = '__all__'

class GeoChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoChart
        fields = '__all__'

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'

class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = '__all__'
