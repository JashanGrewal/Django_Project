from django.shortcuts import render, redirect,render_to_response
from django.http import HttpResponse
from .models import Contractor,labour,Profile
from .mehak import show_labour
from .location_lab import labor_place
from django.contrib.auth import login as auth_login
from .forms import SignUpForm,ProfileForm
import logging
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.template import RequestContext
import sqlite3

logging.basicConfig(filename = "function_logger.log",format='%(asctime)s %(message)s',filemode='w',level=logging.DEBUG)
logger = logging.getLogger(__name__)

def home(request):
    labours = None
    if request.method == 'POST':
        logger.info('entered if')
        pincode = int( request.POST['pincode'])
        req_labour = int(request.POST['req_labour'])
        skill=request.POST['skill']
        logger.debug('pincode is {0} and req_labour is {1}'.format(pincode,req_labour))
        labours = show_labour(pincode,req_labour,skill)
        if (labours==None):
            return render(request,'no_pincode.html')
        if (labours==[]):
            return render(request,'no_labour.html')
        else:
            logger.debug('labours list is {0}'.format(labours))
            return render(request, 'html.html',{'lab':labours})
    else:
        return render(request,'try.html')

def con_profile(request):
    if request.method == 'POST':
        name =request.POST['name']
        contactnumber = request.POST['contactnumber']
        gender = request.POST['gender']
        address = request.POST['address']
        state = request.POST['state']
        city = request.POST['city']
        pincode = request.POST['pincode']

        contractor = Contractor.objects.create(
                name = name,
                contactnumber = contactnumber,
                gender = gender,
                address = address,
                state = state,
                city = city,
                pincode = pincode
                )
        return redirect('home')
    return render(request,'con_profile.html')


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect('update_profile')
        else:
            form = SignUpForm()
        return render(request, 'con_signup.html', {'form': form})
    else:
        return redirect('home')

def labour_signup(request):
    lab = None
    if request.method == 'POST':
        name = request.POST['name']
        contactnumber = int(request.POST['contactnumber'])
        skills = request.POST['skills']
        gender = request.POST['gender']
        address = request.POST['address']
        state = request.POST['state']
        city = request.POST['city']
        pincode = int(request.POST['pincode'])
        place = labor_place(pincode)
        con = sqlite3.connect('/home/mehakpreet/ppcrc/testposition/prcatice/full_data_labour.sqlite3')
        cur = con.cursor()
        cur.execute("INSERT INTO labour(contact_no,pin,name,place,skills,gender,address,city,state) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(contactnumber,pincode,name,place,skills,gender,address,city,state))
        con.commit()
        con.close()
        return render(request,'success.html')
    return render(request,'labour_signup.html')

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        logger.info('entered if')
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            logger.info('valid user form')
            profile_form.save()
            logger.info('valid profile form')
            messages.success(request,'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'profile_form': profile_form})

@login_required
def profile_view(request):
    return render(request,'profile_view.html')



