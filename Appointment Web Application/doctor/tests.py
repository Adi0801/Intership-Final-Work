from django.test import TestCase
from django.urls import reverse
from .models import Appointment
class AppointmentModelTest(TestCase):

    def test_create_appointment(self):
        appointment = Appointment.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890",
            request="Test appointment"
        )
        self.assertEqual(appointment.first_name, "John")
        self.assertEqual(appointment.last_name, "Doe")
        self.assertEqual(appointment.email, "john@example.com")
        self.assertEqual(appointment.phone, "1234567890")
        self.assertEqual(appointment.request, "Test appointment")
    

    def test_create_appointment_with_timeslot(self):
        appointment = Appointment.objects.create(
            first_name="Alice",
            last_name="Johnson",
            email="alice@example.com",
            phone="5555555555",
            request="Test appointment with timeslot",
            timeslot="morning"
        )
        self.assertEqual(appointment.timeslot, "morning")

    def test_create_appointment_with_doctor(self):
        appointment = Appointment.objects.create(
            first_name="Bob",
            last_name="Brown",
            email="bob@example.com",
            phone="1111111111",
            request="Test appointment with doctor",
            doctor="Dr. Raj"
        )
        self.assertEqual(appointment.doctor, "Dr. Raj")
 


class AppointmentViewTest(TestCase):

    def test_appointment_view_get(self):
        response = self.client.get(reverse('appointment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointment.html')

    def test_appointment_view_post(self):
        data = {
            'fname': 'John',
            'lname': 'Doe',
            'email': 'john@example.com',
            'mobile': '1234567890',
            'request': 'Test appointment'
        }
        response = self.client.post(reverse('appointment'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Appointment.objects.filter(first_name='John').exists())

    def test_appointment_view_invalid_form(self):
        data = {
            'fname': 'Aditya',
            'email': 'invalid-email',
        }
        response = self.client.post(reverse('appointment'), data)
        self.assertEqual(response.status_code, 200)  # Form is invalid, should return the same page
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')



