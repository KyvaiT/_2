from django.contrib import admin
from .models import Main, DemandChart, GeoChart, Skills, Statistic

@admin.register(Main)
class MainAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image')
    search_fields = ('title',)

@admin.register(DemandChart)
class DemandChartAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
    search_fields = ('title',)

@admin.register(GeoChart)
class GeoChartAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
    search_fields = ('title',)

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ('year', 'skills')
    search_fields = ('year',)

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('year', 'average_salary', 'vacancy_count')
    search_fields = ('year',)
