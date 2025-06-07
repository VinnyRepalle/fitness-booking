from rest_framework import serializers
from rest_framework.fields import DateTimeField
from django.utils import timezone
from .models import FitnessClass,Booking  
from django.utils import timezone
import pytz
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
import logging


class FitnessClassSerializer(serializers.ModelSerializer):
    
    fitness_class_name = serializers.CharField(write_only=True, required=False)
    class_datetime = serializers.DateTimeField(
        write_only=True,
        input_formats=['%d/%m/%Y %H:%M', '%d/%m/%Y %I:%M %p'],
        required=True
    )

    
    name = serializers.CharField(read_only=True)
    datetime = serializers.DateTimeField(
        read_only=True,
        format='%d/%m/%Y %I:%M %p'  
    )
    instructor = serializers.CharField()
    available_slots = serializers.IntegerField()

    is_upcoming = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = [
            'id', 'name', 'fitness_class_name', 'class_datetime',
            'datetime', 'instructor', 'available_slots', 'is_upcoming'
        ]

    def create(self, validated_data):
        name = validated_data.pop('fitness_class_name', None)
        class_datetime = validated_data.pop('class_datetime', None)

        
        if not name:
            raise serializers.ValidationError({"fitness_class_name": "This field is required."})

        if not class_datetime:
            raise serializers.ValidationError({"class_datetime": "This field is required."})

        return FitnessClass.objects.create(
            name=name,
            datetime=class_datetime,
            instructor=validated_data['instructor'],
            available_slots=validated_data.get('available_slots', 0)
        )

    def get_is_upcoming(self, obj):
        return obj.datetime >= timezone.now()




class BookingSerializer(serializers.ModelSerializer):
   
    fitness_class = serializers.PrimaryKeyRelatedField(
        queryset=FitnessClass.objects.filter(datetime__gte=timezone.now()),
        write_only=True
    )
    fitness_class_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'fitness_class', 'fitness_class_display', 'client_name', 'client_email']

    
    def get_fitness_class_display(self, obj):
        return f"{obj.fitness_class.name} - {obj.fitness_class.datetime.strftime('%d/%m/%Y %I:%M %p')}"

    def validate_fitness_class(self, value):
        if value.available_slots < 1:
            raise serializers.ValidationError("No available slots for this class.")
        return value
