from django.urls import path
from doctor import views
from .views import HomeTemplateView, AppointmentTemplateView, ManageAppointmentTemplateView

urlpatterns = [
    path('',views.register, name='register'),
    path('login',views.Login,name='login'),
    path('home/logout',views.Logout,name='logout'),
    path("home/", HomeTemplateView.as_view(), name="home"),
    # path("home/", HomeTemplateView.as_view(), name="home"),
    path("make-an-appointment/", AppointmentTemplateView.as_view(), name="appointment"),
    path("manage-appointments/", ManageAppointmentTemplateView.as_view(), name="manage"),
]
