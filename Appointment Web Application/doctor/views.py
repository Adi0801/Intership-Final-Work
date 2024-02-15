from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage, message
from django.conf import settings
from django.contrib import messages
from .models import Appointment,profile
from django.views.generic import ListView
import datetime
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login,logout

def Login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password is wrong!')
            # return HttpResponse("Username and password are not correct!!!")
    return render(request,'login.html') #this is important line for not geeting value error 
       
def Logout(request):
    logout(request)
    return redirect('login')

def register(request):
   if request.method=='POST':
    #    name = request.POST['name']
    #    lastname = request.POST['lastname']
       uname = request.POST['username']
       email = request.POST['email']
       pass1 = request.POST['password']
       pass2 = request.POST['password2']
    
       
       if pass1 != pass2:
           return HttpResponse("Your Paasword is not same")
       else:
           my_user=User.objects.create_user(uname,email,pass1)
           my_user.save()
           return redirect('login')
   else:
       return render(request, 'register.html')
    
       
    
    


class HomeTemplateView(TemplateView):
    template_name = "index.html" #for rendering
    
    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        # recipient_email = request.POST.get("email")

        email = EmailMessage(
            subject= f"{name} Notification From RailwayHealthCeneter.",
            body=message,
            # from_email=email,
            from_email=settings.EMAIL_HOST_USER,
            # to=[settings.EMAIL_HOST_USER],
            to=[email], 
            reply_to=[email]
            # settings.EMAIL_HOST_USER,
            # [appointment.email],

        )
       
        email.send()
        # return HttpResponse("Email sent successfully!")
        return HttpResponseRedirect(request.path)


class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"

    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("fname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")
        timeslot = request.POST.get("timeslot")
        doctor=request.POST.get("doctor") 

        #instance of appointment and variable inside instance display in admin or in db

        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=message,
            timeslot=timeslot,
            doctor=doctor,
        )

        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for making an appointment, we will email you ASAP!")
        return HttpResponseRedirect(request.path)

class ManageAppointmentTemplateView(ListView):
    template_name = "manage-appointments.html"
    model = Appointment
    context_object_name = "appointments"
    login_required = True
    paginate_by = 3 #to represent object in one page


    def post(self, request):
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.accepted = True
        appointment.accepted_date = datetime.datetime.now()
        appointment.save()

        data = {
            "fname":appointment.first_name,
            "date":date,
            "doctor":appointment.doctor,
        }

        message = get_template('email.html').render(data)
        email = EmailMessage(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.email],
        )
        email.content_subtype = "html"
        email.send()

        messages.add_message(request, messages.SUCCESS, f"You accepted the appointment of {appointment.first_name}")
        return HttpResponseRedirect(request.path)

#for fetching content from appointment page
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({   
            "title":"Manage Appointments"
        })
        return context

