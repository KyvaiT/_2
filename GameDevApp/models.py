from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

class Main(models.Model):
    title = models.CharField('Название профессии', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Картинка', blank=True, upload_to='pictures/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"

class DemandChart(models.Model):
    title = models.CharField('Название графика', max_length=100)
    image = models.ImageField('График', upload_to='charts/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'График востребованности'
        verbose_name_plural = 'Графики востребованности'

class GeoChart(models.Model):
    title = models.CharField('Название графика', max_length=100)
    image = models.ImageField('График', upload_to='charts/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'График географии'
        verbose_name_plural = 'Графики географии'

class Skills(models.Model):
    year = models.CharField('Год', max_length=4)
    skills = models.TextField('Навыки')

    def __str__(self):
        return self.year

    class Meta:
        verbose_name = 'Ключевой навыки'
        verbose_name_plural = 'Ключевой навыки'

class Statistic(models.Model):
    year = models.IntegerField()
    average_salary = models.FloatField()
    vacancy_count = models.IntegerField()
    city = models.CharField(max_length=100)
    city_salary = models.FloatField()
    city_vacancy_percentage = models.FloatField()
    top_skills = models.TextField()

    def __str__(self):
        return f"{self.year} - {self.average_salary} - {self.vacancy_count}"

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистики'
