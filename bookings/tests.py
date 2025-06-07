from django.test import TestCase
from .serializers import FitnessClassSerializer 
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from rest_framework import status
from .serializers import BookingSerializer
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Booking, FitnessClass



class FitnessClassListTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('fitness-class-list')  

        
        self.past_class = FitnessClass.objects.create(
            name="Past Yoga",
            description="Old session",
            datetime=timezone.now() - timezone.timedelta(days=1)
        )

        
        self.future_class = FitnessClass.objects.create(
            name="Future Zumba",
            description="Upcoming session",
            datetime=timezone.now() + timezone.timedelta(days=1)
        )

    def test_get_upcoming_fitness_classes_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = FitnessClassSerializer([self.future_class], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_no_upcoming_fitness_classes(self):
        FitnessClass.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_internal_server_error_handling(self):
        from unittest.mock import patch

        with patch('your_app.views.FitnessClass.objects.filter') as mock_filter:
            mock_filter.side_effect = Exception("Database Error")
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "An error occurred while retrieving classes.")

#===================================================================#




def test_create_fitness_class_success():
    
    admin_user = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
    
    
    client = APIClient()
    client.login(username='admin', password='adminpass')

    url = reverse('fitness_class_create') 
    data = {
        "name": "Zumba",
        "datetime": (datetime.now() + timedelta(days=1)).isoformat(),
        "instructor": "John Doe",
        "available_slots": 10
    }

    response = client.post(url, data, format='json')
    
    assert response.status_code == 201
    assert "Fitness class" in response.data
    assert response.data["Available slots"] == 10


def test_create_fitness_class_invalid_data():
    admin_user = User.objects.create_user(username="admin", password="adminpass", is_staff=True)

    client = APIClient()
    client.login(username='admin', password='adminpass')

    url = reverse('fitness_class_create')
    data = {
        "name": "",  
        "datetime": "",  
        "instructor": "",
        "available_slots": -5 
    }

    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "name" in response.data or "available_slots" in response.data

#===================================================================#



class BookingCreateTest(APITestCase):

    def setUp(self):
        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            datetime=timezone.now() + timezone.timedelta(days=1),
            available_slots=5
        )
        self.valid_payload = {
            "fitness_class": self.fitness_class.id,
            "client_name": "John Doe"
        }
        self.url = reverse('booking-create')  

    def test_successful_booking_creation(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.fitness_class.refresh_from_db()
        self.assertEqual(self.fitness_class.available_slots, 4)

    def test_booking_with_no_available_slots(self):
        self.fitness_class.available_slots = 0
        self.fitness_class.save()

        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No available slots", str(response.data))

    def test_booking_without_fitness_class(self):
        invalid_payload = {
            "client_name": "John Doe"
        }
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Fitness class is required", str(response.data))



#=========================================================================#



class BookingListByEmailTest(APITestCase):

    def setUp(self):
        self.fitness_class = FitnessClass.objects.create(
            name="Zumba",
            datetime=timezone.now() + timezone.timedelta(days=1),
            available_slots=3
        )
        self.booking1 = Booking.objects.create(
            fitness_class=self.fitness_class,
            client_email="user@example.com",
            client_name="User One"
        )
        self.booking2 = Booking.objects.create(
            fitness_class=self.fitness_class,
            client_email="user@example.com",
            client_name="User One"
        )
        self.booking_other = Booking.objects.create(
            fitness_class=self.fitness_class,
            client_email="other@example.com",
            client_name="User Two"
        )
        self.url = reverse('booking-list-by-email') 

    def test_get_bookings_by_email_success(self):
        response = self.client.get(self.url, {'email': 'user@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 
        emails = {booking['client_email'] for booking in response.data}
        self.assertIn('user@example.com', emails)

    def test_get_bookings_missing_email_param(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Email parameter is required.")
