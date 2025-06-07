Fitness Studio Booking API

sample REST API for booking fitness classes like Yoga, Zumba, and HIIt at a fictional fitness studio including API design input validation,error handling and timezone management.

Features:

1. view all upcoming fitness classes
2. Book a class by providing name,email and class name
3. Retrive bookings by email
4. Handles overbooking and missing data gracefully
5. Timezone-aware class schedules (IST by default)

Running the project (Django)

First ensure that a virtual environment venv exists.if not, create one using the steps below.

A virtual environment is used to isolate project dependencies so they don't affect the global python environment
 
Steps:

1. Create the virtual environment
    The following command creates a venv folder containing all the project dependencies:

        python -m venv env

2. Activate the virtual environment
    On Windows,use:

        venv\Scripts\activate

3. Navigate to the project directory
    Make sure you are in the same directory where manage.py is located.

4. Install dependencies
    If requirements.txt is present, Install all required packages using:

        pip install -r requirements.txt

5. Run database migrations
    To apply migrations and set up the database schema:

        python manage.py makemigrations
        python manage.py migrate

6. Creating an Admin User
   To access the Django admin panel or manage data securely,you will need to create a superuser
    Run the following command:

        python manage.py createsuperuser

    we have to remember the username and password

    Username (leave blank to use "vinny"):
    Email address:
    Password:
    Password(again):
    This password is too short. It must contain at least 8 characters.
    This password is too common.
    This password is entirely numeric.
    Bypass password validation and create user anyway? [y/N]:y
    Superuser created successfully.

7. Start the development server
    Launch the Django development server with

        python manage.py runserver



PROJECT STRUCTURE

| Route                                      | Description                                                   |
|-------------------------------------------|---------------------------------------------------------------|
| create/classes/                        | This route is for creating a fitness class.                   |
| classes/                                | Lists upcoming classes with name, time, instructor, and slots.|
| book/                                   | Books a class if slots are available, then reduces slot count.|
| bookings/?email=example@gmail.com       | Returns all bookings made by a specific email address.        |



USE 
To test the API'S
First,start Django's development server.

python manage.py runserver

1. create/classes/
    This is a POST endpoint used to add new fitness classes,Before using this endpoint ,you must first create method by sending the following JSON payload:

    This is the route to create the classes

    http://127.0.0.1:8000/create/classes/

    payload

    {
     "Fitness class": "Zumba",
     "date time": "23/06/2025 06:30 AM",
     "Instructor": "John Doe",
     "Available slots": 20
   }

it will create fitness classes

2. classes/
This is the get method whatever the classes we created we can see that classes using this route.
    this is the route for Lists upcoming classes with name,time,instructor, and slots.

OUTPUT:
[
    {
        "id": 19,
        "name": "Zumba",
        "datetime": "14/06/2025 06:30 AM",
        "instructor": "John Doe",
        "available_slots": 19,
        "is_upcoming": true
    },
    {
        "id": 20,
        "name": "Zumba",
        "datetime": "15/06/2025 06:30 AM",
        "instructor": "John Doe",
        "available_slots": 19,
        "is_upcoming": true
    },
    {
        "id": 21,
        "name": "Zumba",
        "datetime": "23/06/2025 06:30 AM",
        "instructor": "John Doe",
        "available_slots": 20,
        "is_upcoming": true
    }
]

3. book/
This is the post method to book the classes which are available if the slots are not available that class data
    this is the route for Books a class if slots available.

    http://127.0.0.1:8000/book/

this one response i was attached image.png

4. bookings/?email=example@gmail.com/
it will return the data for the particular email how many classes that user want to join
    This is the route to create the classes

    http://127.0.0.1:8000/bookings/?email=vineetha123@gmail.com

OUTPUT:
[
    {
        "id": 18,
        "fitness_class_display": "Zumba - 14/06/2025 01:00 AM",
        "client_name": "vinny",
        "client_email": "vineetha123@gmail.com"
    },
    {
        "id": 19,
        "fitness_class_display": "Zumba - 15/06/2025 01:00 AM",
        "client_name": "vinny",
        "client_email": "vineetha123@gmail.com"
    },
    {
        "id": 20,
        "fitness_class_display": "Zumba - 23/06/2025 01:00 AM",
        "client_name": "vinny",
        "client_email": "vineetha123@gmail.com"
    }
]
