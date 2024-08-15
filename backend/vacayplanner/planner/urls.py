from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, FlightViewSet, EventViewSet, ItineraryViewSet

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'events', EventViewSet)
router.register(r'itineraries', ItineraryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('flights/fetch/', FlightViewSet.as_view({'get': 'fetch_flight_data'}), name='fetch-flight-data'),
    path('events/fetch/', EventViewSet.as_view({'get': 'fetch_events'}), name='fetch-events'),
    path('itineraries/generate/', ItineraryViewSet.as_view({'get': 'generate_itinerary'}), name='generate-itinerary'),
    # Add paths for other API integrations as needed
]
