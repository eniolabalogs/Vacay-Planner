from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from .models import UserProfile, Flight, Event, Itinerary
from .serializers import UserProfileSerializer, FlightSerializer, EventSerializer, ItinerarySerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    @action(detail=False, methods=['get'])
    def fetch_flight_data(self, request):
        flight_number = request.query_params.get('flight_number')
        response = requests.get(f"http://api.aviationstack.com/v1/flights?access_key=ac6f9f44569cd29f2e10e9753853774a&flight_iata={flight_number}")
        flight_data = response.json()
        
        if flight_data['data']:
            flight_info = flight_data['data'][0]
            flight, created = Flight.objects.update_or_create(
                flight_number=flight_info['flight']['iata'],
                defaults={
                    'departure_time': flight_info['departure']['estimated'],
                    'arrival_time': flight_info['arrival']['estimated'],
                    'airline': flight_info['airline']['name'],
                    'status': flight_info['flight_status']
                }
            )
            return Response(FlightSerializer(flight).data)
        else:
            return Response({"error": "Flight not found"}, status=404)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=False, methods=['get'])
    def fetch_events(self, request):
        location = request.query_params.get('location')
        response = requests.get(f"https://api.eventful.com/json/events/search?location={location}&app_key=YOUR_EVENTFUL_API_KEY")
        events_data = response.json()

        for event_info in events_data['events']['event']:
            Event.objects.update_or_create(
                event_id=event_info['id'],
                defaults={
                    'event_name': event_info['title'],
                    'event_date': event_info['start_time'],
                    'location': event_info['venue_address']
                }
            )
        return Response({"status": "Events updated"})

class ItineraryViewSet(viewsets.ModelViewSet):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

    @action(detail=False, methods=['get'])
    def generate_itinerary(self, request):
        user_id = request.query_params.get('user_id')
        user = UserProfile.objects.get(id=user_id)

        # Fetch weather data from OpenWeatherMap
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user.location}&appid=YOUR_OPENWEATHERMAP_API_KEY")
        weather_data = response.json()

        # Fetch places of interest from Google Places API
        response = requests.get(f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={user.location}&radius=1500&type=point_of_interest&key=YOUR_GOOGLE_PLACES_API_KEY")
        places_data = response.json()

        # Fetch flights and events (already implemented above)
        # Process and generate itinerary based on the user's preferences

        itinerary = Itinerary.objects.create(
            user=user,
            weather_forecast=weather_data,
            places_of_interest=places_data['results']
        )

        return Response(ItinerarySerializer(itinerary).data)

