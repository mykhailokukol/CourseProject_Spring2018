from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *
from . import models
from django.conf import settings
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test

# AUTH PAGES VIEWS

def signup(request):
    logout(request)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.refresh_from_db()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/home/')
    else:
        form = SignUpForm()
    return render(request, 'auth/sign_up.html', { 'form': form })

def login_page(request):
    logout(request)
    username = password = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/home/')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

# INDEX (HOME) PAGE VIEWS

def index(request):
    return render(request, 'main/index.html')

# TASK VIEWS

def tasks(request):
    return render(request, 'main/tasks.html')

# PROFILE VIEWS

# @login_required
def profile(request):
    user = request.user
    accidents_query = models.Profile.objects.raw("select distinct 1 as id, acc.type, datetime, street, house from appmain_fixationaccident fixacc join auth_user au on au.id = %s join appmain_driver drv on drv.human_id = au.id join appmain_drivers drvs on drvs.driver_id = drv.id join appmain_fixationaccident_accident_type fat on fat.fixationaccident_id = fixacc.id join appmain_accident acc on acc.id = fat.accident_id" % (request.user.id))
    acc_types = models.Accident.objects.all()
    # violations_query = models.Profile.objects.raw("select distinct 1 as id, violation_id, datetime, street, house from appmain_drivingviolation dv join appmain_driver drv on drv.id = dv.driver_id join auth_user au on au.id = %s;" % (request.user.id))
    violations_query = models.Profile.objects.raw("select distinct 1 as id, violation_id, datetime, street, house from appmain_drivingviolation dv join auth_user au on au.id = %s join appmain_driver drv on drv.human_id = au.id" % (request.user.id))
    vio_types = models.Violation.objects.all()
    mycars_query = models.Profile.objects.raw("select distinct 1 as id, mark, model, power, engine_capacity, body_type, year, lecinse_plate from appmain_car car join appmain_driver drv on (drv.human_id = %s and car.id = drv.car_id)" % (request.user.id))
    return render(request, 'main/profile.html', {
        'profile': models.Profile.objects.all(),
        'user_id': request.user.id,
        'accidents_query': accidents_query,
        'accidents': acc_types,
        'vio_query': violations_query,
        'vio_types': vio_types,
        'my_cars': mycars_query,
    })

@login_required
def profile_settings(request):
    try:
        if request.method == 'POST' and request.FILES['Photo-avatar']:
            if 'cng_photo' in request.POST:
                PSChangePhoto = PSChangePhotoForm(request.POST, request.FILES, prefix='Photo')
                # Need to be fixed
                # if PSChangePhoto.is_valid():

                # save to project
                photo = request.FILES['Photo-avatar']
                fs = FileSystemStorage()
                filename = fs.save(photo.name, photo)
                print(filename)
                # save to db
                models.Profile.objects.filter(pk=request.user.id).update(avatar=filename)
    except Exception:
        if request.method == 'POST':
            if 'addcar' in request.POST:
                PSAddCar = PSAddCarForm(request.POST, prefix='CarAdding')
                if PSAddCar.is_valid():
                    car = request.POST.get('CarAdding-car')
                    sure = request.POST.get('CarAdding-sure')
                    car = models.Car.objects.filter(pk=car)[0]
                    if sure:
                        car_model = models.Driver(car=car, human=request.user)
                        car_model.save()
            elif 'cng_profile' in request.POST:
                PSChanging = PSChangingForm(request.POST, prefix='Changing')
                # Need to be fixed!
                # if PSChanging.is_valid():
                email = birthday = None
                email = request.POST.get('Changing-email')
                birthday = request.POST.get('Changing-birthday')
                if not email:
                    models.Profile.objects.filter(user_id=request.user.id).update(birthday=birthday)
                elif not birthday:
                    models.User.objects.filter(pk=request.user.id).update(email=email)
                else:
                    models.User.objects.filter(pk=request.user.id).update(email=email)
                    models.Profile.objects.filter(user_id=request.user.id).update(birthday=birthday)
    return render(request, 'main/profile/settings.html', {
        'PhotoChangeForm': PSChangePhotoForm(prefix='Photo'),
        'CarAddingForm': PSAddCarForm(prefix='CarAdding'),
        'ChangingForm': PSChangingForm(prefix='Changing'),
        'profile': models.Profile.objects.all(),
        'user_id': request.user.id,
        'accidents': models.FixationAccident.objects.all(),
        'violations': models.DrivingViolation.objects.all(),
        'drivers': models.Drivers.objects.all(),
        'driver': models.Driver.objects.all(),
        'accident_types': models.Accident.objects.all(),
    })

# CONTROL PAGE

@login_required
@user_passes_test(lambda u: u.groups.filter(name='inspectors').exists(), login_url='/access_denied/')
def control(request):
    return render(request, 'main/control.html')

# CONTROL PAGE VIEWS

@login_required
@user_passes_test(lambda u: u.groups.filter(name='inspectors').exists(), login_url='/access_denied/')
def send_email(request):
    if request.method == 'POST':
        SendEmail = SendEmailForm(request.POST)
        if SendEmail.is_valid():
            username = request.POST.get('user')
            user = models.User.objects.filter(pk=username)[0]
            subject = request.POST.get('subject', '<Дефолтная тема письма>')
            data = request.POST.get('data', '<here should be some text>')
            send_mail(user.email, data, 'kukol.dbcp.django@gmail.com', [user.email])
    else:
        SendEmail = SendEmailForm()
    return render(request, 'main/control/send_email.html', { 'SendEmailForm': SendEmail })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='inspectors').exists(), login_url='/access_denied/')
def accs_info(request):
    if request.method == 'POST':
        type = None
        if 'add' in request.POST:
            AddAccident = AddAccidentForm(request.POST, prefix='Adding')
            if AddAccident.is_valid():
                type = request.POST.get('Adding-type')
                accident = models.Accident(type=type)
                accident.save()
        elif 'change' in request.POST:
            ChangeAccident = ChangeAccidentForm(request.POST, prefix='Changing')
            # if ChangeAccident.is_valid():

            # ИСПРАВИТЬ ПРОБЛЕМУ С ВАЛИДАЦИЕЙ!!!

            accident = request.POST.get('Changing-accident')
            type = request.POST.get('Changing-type')
            models.Accident.objects.filter(type=accident).update(type=type)
        elif 'delete' in request.POST:
            DeleteAccident = DeleteAccidentForm(request.POST, prefix='Deleting')
            # if DeleteAccident.is_valid():
            accident = request.POST.get('Deleting-accident')
            models.Accident.objects.filter(type=accident).delete()
    return render(request, 'main/control/accs_info.html', {'AddAccidentForm': AddAccidentForm(prefix='Adding'), 'ChangeAccidentForm': ChangeAccidentForm(prefix='Changing'), 'DeleteAccidentForm': DeleteAccidentForm(prefix='Deleting'), })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='inspectors').exists(), login_url='/access_denied/')
def fixate_accident(request):
    if request.method == 'POST':
        FixateAccident = FixateAccidentForm(request.POST)
        if FixateAccident.is_valid():
            street = request.POST.get('street')
            house = request.POST.get('house')
            type = request.POST.get('type')
            datetime = request.POST.get('datetime')
            drivers_list = FixateAccident.cleaned_data['drivers']
            print(drivers_list)
            try:
                pedestrians_list = FixateAccident.cleaned_data['pedestrians']
            except Exception:
                pedestrians_list = None
            na_pedestrians_list = request.POST.get('na_pedestrians')
            if not na_pedestrians_list:
                fixated_accident = models.FixationAccident(street=street, house=house, datetime=datetime)
                fixated_accident.save()
                fixacc_last_id = models.FixationAccident.objects.latest('id') # нужна ли эта строка? Или стоит использовать 'fixated_accident'?
                for driver in drivers_list:
                    accident_driver = models.Drivers(driver=driver, fixated_accident=fixacc_last_id)
                    accident_driver.save()
                if pedestrians_list is not None:
                    for pedestrian in pedestrians_list:
                        accident_pedestrian = models.Pedestrians(human=pedestrian, fixated_accident=fixacc_last_id)
                        accident_pedestrian.save()
                fixacc_last_id.accident_type.add(type)
                print(street, house, type, datetime, drivers_list, pedestrians_list)
            else:
               print(street, house, type, datetime, drivers_list, pedestrians_list, na_pedestrians_list)
    else:
        FixateAccident = FixateAccidentForm()
    return render(request, 'main/control/fixate_accident.html', { 'FixateAccidentForm': FixateAccident })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='inspectors').exists(), login_url='/access_denied/')
def fixate_violation(request):
    if request.method == 'POST':
        FixateViolation = FixateViolationForm(request.POST)
        if FixateViolation.is_valid():
            street = request.POST.get('street')
            house = request.POST.get('house')
            type = FixateViolation.cleaned_data['type']
            datetime = request.POST.get('datetime')
            car = FixateViolation.cleaned_data['car']
            print(street, house, type, datetime, car)
            fixvio = models.DrivingViolation(street=street, house=house, datetime=datetime, car=car, violation=type)
            fixvio.save()
    else:
        FixateViolation = FixateViolationForm()
    return render(request, 'main/control/fixate_violation.html', { 'FixateViolationForm': FixateViolation })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='inspectors').exists(), login_url='/access_denied/')
def owners_info(request):
    if request.method == 'POST':
        OwnerInfo = OwnerInfoForm(request.POST)
        if OwnerInfo.is_valid():
            owner = OwnerInfo.cleaned_data['owner']
            owner = owner.username
            accidents_query = models.Profile.objects.raw("select distinct 1 as id, acc.type, datetime, street, house from appmain_fixationaccident fixacc join auth_user au on au.username = '%s' join appmain_driver drv on drv.human_id = au.id join appmain_drivers drvs on drvs.driver_id = drv.id join appmain_fixationaccident_accident_type fat on fat.fixationaccident_id = fixacc.id join appmain_accident acc on acc.id = fat.accident_id" % (owner))
            acc_types = models.Accident.objects.all()
            violations_query = models.Profile.objects.raw("select distinct 1 as id, violation_id, datetime, street, house from appmain_drivingviolation dv join auth_user au on au.username = '%s' join appmain_driver drv on drv.human_id = au.id" % (owner))
            vio_types = models.Violation.objects.all()
    else:
        OwnerInfo = OwnerInfoForm()
        acc_types = vio_types = violations_query = accidents_query = owner = None
    return render(request, 'main/control/owners_info.html', {
        'OwnerInfoForm': OwnerInfo,
        'accidents_query': accidents_query,
        'accidents': acc_types,
        'vio_query': violations_query,
        'vio_types': vio_types,
        'user_id': owner,
    })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='inspectors').exists(), login_url='/access_denied/')
def top_cars(request):
    top_cars_query = models.Car.objects.raw('select 1 as id, mark, model, lecinse_plate, cnt from top_cars_acc')
    return render(request, 'main/control/top_cars.html', { 'query': top_cars_query })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='inspectors').exists(), login_url='/access_denied/')
def top_streets_acc(request):
    top_streets_acc_query = models.FixationAccident.objects.raw('select 1 as id, street, cnt from top_streets_acc')
    return render(request, 'main/control/top_streets_acc.html', { 'query': top_streets_acc_query })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='inspectors').exists(), login_url='/access_denied/')
def top_streets_vio(request):
    top_streets_vio_query = models.DrivingViolation.objects.raw('select 1 as id, street, cnt from top_streets_vio')
    return render(request, 'main/control/top_streets_vio.html', { 'query': top_streets_vio_query })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='inspectors').exists(), login_url='/access_denied/')
def violators(request):
    user = request.user
    violators_query = models.DrivingViolation.objects.raw("select distinct 1 as id, last_name, first_name from auth_user au join appmain_driver drv on drv.human_id = au.id join appmain_car car on car.id = drv.car_id join appmain_drivingviolation vio on drv.car_id = vio.car_id")
    return render(request, 'main/control/violators.html', { 'violators_query': violators_query })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='inspectors').exists(), login_url='/access_denied/')
def vios_info(request):
    if request.method == 'POST':
        type = fine = None
        if 'add' in request.POST:
            AddViolation = AddViolationForm(request.POST, prefix='Adding')
            if AddViolation.is_valid():
                type = request.POST.get('Adding-type')
                fine = request.POST.get('Adding-fine')
                violation = models.Violation(type=type, fine=fine)
                violation.save()
        elif 'change' in request.POST:
            ChangeViolation = ChangeViolationForm(request.POST, prefix='Changing')
            # if ChangeViolation.is_valid():

            # ИСПРАВИТЬ ПРОБЛЕМУ С ВАЛИДАЦИЕЙ!!!

            violation = request.POST.get('Changing-violation')
            type = request.POST.get('Changing-type')
            fine = request.POST.get('Changing-fine')
            models.Violation.objects.filter(type=violation).update(type=type, fine=fine)
        elif 'delete' in request.POST:
            DeleteViolation = DeleteViolationForm(request.POST, prefix='Deleting')
            # if DeleteViolation.is_valid():
            violation = request.POST.get('Deleting-violation')
            models.Violation.objects.filter(type=violation).delete()
    return render(request, 'main/control/vios_info.html', {'AddViolationForm': AddViolationForm(prefix='Adding'), 'ChangeViolationForm': ChangeViolationForm(prefix='Changing'), 'DeleteViolationForm': DeleteViolationForm(prefix='Deleting'), })

# ERRORS PAGES VIEWS

def access_denied(request):
    return render(request, 'main/errors/access_denied.html')
