from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Car)
admin.site.register(Violation)
admin.site.register(Accident)
admin.site.register(FixationAccident)
admin.site.register(Driver)
admin.site.register(DrivingViolation)
admin.site.register(Drivers)
admin.site.register(Pedestrians)
