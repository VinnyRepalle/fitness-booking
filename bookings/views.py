from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.schemas import AutoSchema
from rest_framework.compat import coreapi, coreschema
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from django.utils import timezone
from django.contrib.auth import authenticate

from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from .serializers import FitnessClassSerializer  
import logging
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import FitnessClass


logger = logging.getLogger(__name__)



class FitnessClassList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            classes = FitnessClass.objects.filter(datetime__gte=timezone.now())
            serializer = FitnessClassSerializer(classes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving fitness classes: {str(e)}")
            return Response(
                {"error": "An error occurred while retrieving classes."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FitnessClassCreateAdmin(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = FitnessClassSerializer(data=request.data)
        if serializer.is_valid():
            fitness_class = serializer.save()
            response_data = {
                "Fitness class": fitness_class.name,
                "date time": fitness_class.datetime.strftime('%d/%m/%Y %I:%M %p'),
                "Instructor": fitness_class.instructor,
                "Available slots": fitness_class.available_slots
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingCreate(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        try:
            fitness_class = serializer.validated_data.get('fitness_class')

            if not fitness_class:
                raise serializers.ValidationError("Fitness class is required.")

            if fitness_class.available_slots < 1:
                raise serializers.ValidationError("No available slots for this class.")

            fitness_class.available_slots -= 1
            fitness_class.save()
            serializer.save()

        except serializers.ValidationError as ve:
            logger.warning(f"Validation error during booking: {ve}")
            raise ve  

        except Exception as e:
            logger.error(f"Unexpected error during booking creation: {str(e)}")
            raise serializers.ValidationError("An unexpected error occurred. Please try again later.")


class BookingListByEmail(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({"error": "Email parameter is required."}, status=400)

        tz_name = request.query_params.get('timezone', 'Asia/Kolkata')

        bookings = Booking.objects.filter(client_email=email)
        serializer = BookingSerializer(bookings, many=True, context={'timezone': tz_name})
        return Response(serializer.data)



