from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, FixateAccidentForm, AddViolationForm, SendEmailForm
from . import models
from django.conf import settings
from django.core.mail import send_mail

# AUTH PAGES VIEWS

def signup(request):
    logout(request)
    uploaded_file_url = ''
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
    return render(request, 'auth/sign_up.html', {'form': form, 'uploaded_file_url': uploaded_file_url})

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

def profile(request):
    user = request.user
    accidents_query = models.Profile.objects.raw("select distinct 1 as id, acc.type, datetime, street, house from appmain_fixationaccident fixacc join auth_user au on au.id = %s join appmain_driver drv on drv.human_id = au.id join appmain_drivers drvs on drvs.driver_id = drv.id join appmain_fixationaccident_accident_type fat on fat.fixationaccident_id = fixacc.id join appmain_accident acc on acc.id = fat.accident_id" % (request.user.id))
    acc_types = models.Accident.objects.all()
    violations_query = models.Profile.objects.raw("select distinct 1 as id, violation_id, datetime, street, house from appmain_drivingviolation dv join appmain_driver drv on drv.id = dv.driver_id join auth_user au on au.id = %s;" % (request.user.id))
    vio_types = models.Violation.objects.all()
    mycars_query = models.Profile.objects.raw("select distinct 1 as id, mark, model, power, engine_capacity, body_type, year, lecinse_plate from appmain_car car join appmain_driver drv on drv.human_id = %s" % (request.user.id))
    return render(request, 'main/profile.html', {
        'profile': models.Profile.objects.all(),
        'user_id': request.user.id,
        'accidents_query': accidents_query,
        'accidents': acc_types,
        'vio_query': violations_query,
        'vio_types': vio_types,
        'my_cars': mycars_query,
    })

def profile_settings(request):
    return render(request, 'main/profile/settings.html', {
        'profile': models.Profile.objects.all(),
        'user_id': request.user.id,
        'accidents': models.FixationAccident.objects.all(),
        'violations': models.DrivingViolation.objects.all(),
        'drivers': models.Drivers.objects.all(),
        'driver': models.Driver.objects.all(),
        'accident_types': models.Accident.objects.all(),
    })

# CONTROL PAGE

def control(request):
    if request.method == 'POST':
        FixateAccident = FixateAccidentForm(request.POST, prefix='fixateaccform')
        AddViolation = AddViolationForm(request.POST, prefix='addvioform')
        if FixateAccident.is_valid():
            print(FixateAccidentForm)
        if AddViolation.is_valid():
            type = request.POST.get('add_vio_type')
            fine = request.POST.get('add_vio_fine')
            print('Type: %s\nFine: %s' % (type, fine))
    else:
        AddViolation = AddViolationForm(prefix='addvioform')
        FixateAccident = FixateAccidentForm(prefix='fixateaccform')
    return render(request, 'main/control.html', {'FixateAccident': FixateAccident, 'AddViolation': AddViolation })

# CONTROL PAGE VIEWS

def send_email(request):
    if request.method == 'POST':
        SendEmail = SendEmailForm(request.POST)
        if SendEmail.is_valid():
            email = request.POST.get('email', 'mykhailokukol@gmail.com')
            subject = request.POST.get('subject', '<Дефолтная тема письма>')
            data = request.POST.get('data', '<here should be some text>')
            send_mail(email, data, 'kukol.dbcp.django@gmail.com', [email])
    else:
        SendEmail = SendEmailForm()
    return render(request, 'main/control/send_email.html', { 'SendEmailForm': SendEmail })

def accs_info(request):
    return render(request, 'main/control/accs_info.html')

def fixate_accident(request):
    return render(request, 'main/control/fixate_accident.html')

def fixate_violation(request):
    return render(request, 'main/control/fixate_violation.html')

def owners_info(request):
    return render(request, 'main/control/owners_info.html')

def top_cars(request):
    return render(request, 'main/control/top_cars.html')

def top_streets_acc(request):
    return render(request, 'main/control/top_streets_acc.html')

def top_streets_vio(request):
    return render(request, 'main/control/top_streets_vio')

def violators(request):
    return render(request, 'main/control/violators.html')

def vios_info(request):
    return render(request, 'main/control/vios_info.html')
