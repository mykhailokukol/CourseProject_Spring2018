from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def get_full_name(self):
    return str('%s %s' % (self.last_name, self.first_name))

User.add_to_class('__str__', get_full_name)

# USER PROFILE
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField(max_length = 100)
    birthday = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='', null=True, blank=True)

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

    def __str__(self):
        return ('%s %s %s' % (self.mark, self.model, self.lecinse_plate))

# НАРУШЕНИЕ ПДД (справочник)
class Violation(models.Model):
    type = models.CharField(max_length=255, unique=True, null=False)
    fine = models.FloatField(null=False)

    def __str__(self):
        return str('%s, %sгрн.' % (self.type, self.fine))

# ДТП (справочник)
class Accident(models.Model):
    type = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return str(self.type)

# ЧЕЛОВЕК + АВТОМОБИЛЬ = ВОДИТЕЛЬ
class Driver(models.Model):
    human = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    car = models.ForeignKey('Car', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str('%s %s (%s)' % (self.human.first_name, self.human.last_name, self.car))

# ВОДИТЕЛЬ СОВЕРШИЛ НАРУШЕНИЕ ПДД
class DrivingViolation(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE, null=False, default=2)
    violation = models.ForeignKey('Violation', on_delete=models.CASCADE, null=False)
    datetime = models.DateTimeField(null=False, auto_now=True)
    street = models.CharField(max_length=100, null=False, default='Улица не указана')
    house = models.CharField(max_length=4, null=False, default='-')

    def __str__(self):
        return str('Авто: %s, Нарушение: %s, Место: %s %s, Дата и время: %s' % (self.car, self.violation, self.street, self.house, self.datetime))

# ФИКСАЦИЯ ДТП
class FixationAccident(models.Model):
    street = models.CharField(max_length=30, null=False)
    house = models.CharField(max_length=4, null=False)
    datetime = models.DateTimeField(null=False)
    accident_type = models.ManyToManyField('Accident')

    def __str__(self):
        return str('Место: %s %s, Тип: %s, Дата и время: %s' % (self.street, self.house, self.accident_type, self.datetime))

class Pedestrians(models.Model):
    human = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    role = models.CharField(max_length=12, null=False)
    fixated_accident = models.ForeignKey('FixationAccident', on_delete=models.CASCADE, null=False) # ВОЗМОЖНО НЕВЕРНО СОЗДАННЫЙ СТОЛБЕЦ

    def __str__(self):
        return str('Пешеход: %s, Роль: %s, в ДТП №%s' % (self.human, self.role, self.fixated_accident))

class Drivers(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, null=False)
    fixated_accident = models.ForeignKey('FixationAccident', on_delete=models.CASCADE, null=False) # ВОЗМОЖНО НЕВЕРНО СОЗДАННЫЙ СТОЛБЕЦ
    role = models.CharField(max_length=12, null=False)

    def __str__(self):
        return str('Водитель: %s, Роль: %s, в ДТП №%s' % (self.driver, self.role, self.fixated_accident))
