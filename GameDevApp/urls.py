from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VacancyViewSet, UserViewSet, MainViewSet, DemandChartViewSet, GeoChartViewSet, SkillsViewSet, StatisticViewSet, index, statistics, demand, geo, skills, vacancies
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'vacancies', VacancyViewSet)
router.register(r'users', UserViewSet)
router.register(r'main', MainViewSet)
router.register(r'demand', DemandChartViewSet)
router.register(r'geo', GeoChartViewSet)
router.register(r'skills', SkillsViewSet)
router.register(r'statistics', StatisticViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('statistics/', statistics, name='statistics'),
    path('demand/', demand, name='demand'),
    path('geo/', geo, name='geo'),
    path('skills/', skills, name='skills'),
    path('vacancies/', vacancies, name='vacancies'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
