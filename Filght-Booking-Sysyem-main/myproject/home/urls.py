from django.urls import path
from . import views

urlpatterns = [
    # Static pages
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    
    # Flight booking
    path('search/', views.flight_search, name='flight_search'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<str:reference>/', views.booking_detail, name='booking_detail'),
    path('cancel/<str:reference>/', views.cancel_booking, name='cancel_booking'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]

