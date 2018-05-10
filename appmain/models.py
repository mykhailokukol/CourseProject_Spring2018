from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# USER PROFILE
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField(max_length = 100)
    birthday = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# АВТОМОБИЛЬ
class Car(models.Model):
    mark = models.CharField(max_length=255, null=False)
    model = models.CharField(max_length=255, null=False)
    power = models.IntegerField(null=False)
    engine_capacity = models.FloatField(max_length=3, null=False)
    body_type = models.CharField(max_length=15, null=False)
    year = models.PositiveSmallIntegerField(null=False)
    lecinse_plate = models.CharField(max_length=10, unique=True, null=False)

# НАРУШЕНИЕ ПДД (справочник)
class Violation(models.Model):
    type = models.CharField(max_length=255, unique=True, null=False)
    fine = models.FloatField(null=False)

# ДТП (справочник)
class Accident(models.Model):
    type = models.CharField(max_length=255, unique=True, null=False)

# ЧЕЛОВЕК + АВТОМОБИЛЬ = ВОДИТЕЛЬ
class Driver(models.Model):
    human = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    car = models.ForeignKey('Car', on_delete=models.CASCADE, null=False)

# ВОДИТЕЛЬ СОВЕРШИЛ НАРУШЕНИЕ ПДД
class DrivingViolation(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE, null=False, default=2)
    violation = models.ForeignKey('Violation', on_delete=models.CASCADE, null=False)
    datetime = models.DateTimeField(null=False, auto_now=True)
    street = models.CharField(max_length=100, null=False, default='Улица не указана')
    house = models.CharField(max_length=4, null=False, default='-')

# ФИКСАЦИЯ ДТП
class FixationAccident(models.Model):
    street = models.CharField(max_length=30, null=False)
    house = models.CharField(max_length=4, null=False)
    datetime = models.DateTimeField(null=False)
    accident_type = models.ManyToManyField('Accident')

class Pedestrians(models.Model):
    human = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    role = models.CharField(max_length=12, null=False)
    fixated_accident = models.ForeignKey('FixationAccident', on_delete=models.CASCADE, null=False) # ВОЗМОЖНО НЕВЕРНО СОЗДАННЫЙ СТОЛБЕЦ

class Drivers(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, null=False)
    fixated_accident = models.ForeignKey('FixationAccident', on_delete=models.CASCADE, null=False) # ВОЗМОЖНО НЕВЕРНО СОЗДАННЫЙ СТОЛБЕЦ
    role = models.CharField(max_length=12, null=False)
