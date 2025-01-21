from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Vacancy, CustomUser, Main, DemandChart, GeoChart, Skills, Statistic
from .serializers import VacancySerializer, UserSerializer, MainSerializer, DemandChartSerializer, GeoChartSerializer, SkillsSerializer, StatisticSerializer
from .parser import Parser

def index(request):
    data = Main.objects.all()
    content = {'data': data}
    return render(request, 'application/index.html', context=content)

def statistics(request):
    data = Statistic.objects.all()
    content = {'data': data}
    return render(request, 'application/../../project/app_professions/templates/app_professions/statistics.html', context=content)

def demand(request):
    data = DemandChart.objects.all()
    content = {'data': data}
    return render(request, 'application/../../project/app_professions/templates/app_professions/demand.html', context=content)

def geo(request):
    data = GeoChart.objects.all()
    content = {'data': data}
    return render(request, 'application/../../project/app_professions/templates/app_professions/geo.html', context=content)

def skills(request):
    data = Skills.objects.all()
    content = {'data': data}
    return render(request, 'application/../../project/app_professions/templates/app_professions/skills.html', context=content)

def vacancies(request):
    data = Parser().parser()
    content = {'data': data}
    return render(request, 'application/../../project/app_professions/templates/app_professions/vacancies.html', context=content)

class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class MainViewSet(viewsets.ModelViewSet):
    queryset = Main.objects.all()
    serializer_class = MainSerializer
    permission_classes = [IsAuthenticated]

class DemandChartViewSet(viewsets.ModelViewSet):
    queryset = DemandChart.objects.all()
    serializer_class = DemandChartSerializer
    permission_classes = [IsAuthenticated]

class GeoChartViewSet(viewsets.ModelViewSet):
    queryset = GeoChart.objects.all()
    serializer_class = GeoChartSerializer
    permission_classes = [IsAuthenticated]

class SkillsViewSet(viewsets.ModelViewSet):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    permission_classes = [IsAuthenticated]

class StatisticViewSet(viewsets.ModelViewSet):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer
    permission_classes = [IsAuthenticated]
