
from django.db import models
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication
from django.utils import timezone
from django.db import models


class FitnessClass(models.Model):
    name = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    available_slots = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.datetime.strftime('%d/%m/%Y %I:%M %p')}"

class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booked_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.client_name} booked {self.fitness_class.name}"
