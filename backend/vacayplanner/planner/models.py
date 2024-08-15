from django.db import models

# Create your models here.
class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    preferences = models.JSONField()

    def __str__(self):
        return self.name

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airline = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.flight_number

class Event(models.Model):
    event_id = models.CharField(max_length=255)
    event_name = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.event_name

class Itinerary(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    flights = models.ManyToManyField(Flight)
    events = models.ManyToManyField(Event)
    weather_forecast = models.JSONField()
    places_of_interest = models.JSONField()

    def __str__(self):
        return f"Itinerary for {self.user.name}"
