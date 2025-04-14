from django.contrib import admin
from django.urls import path
from home import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path('service',views.service, name='service'),
    path("contact", views.contact,name ='contact'),
     # Home and searchpy
    #path('', views.home, name='home'),
    path('search/', views.flight_search, name='flight_search'),
   # path('search_results', views.search_results, name='search_results'),
    
    # Booking process
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('booking/<str:reference>/', views.booking_detail, name='booking_detail'),
     path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    
    # User account
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<str:reference>/', views.cancel_booking, name='cancel_booking'),
   # path('profile/', views.user_profile, name='user_profile'),
    
    # Static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)








''' path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path('service',views.service, name='service'),
    path("contact", views.contact,name ='contact'),
     # Home and searchpy
    #path('', views.home, name='home'),
    path('search/', views.flight_search, name='flight_search'),
   # path('search_results', views.search_results, name='search_results'),
    
    # Booking process
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('booking/<str:reference>/', views.booking_detail, name='booking_detail'),
     path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    
    # User account
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<str:reference>/', views.cancel_booking, name='cancel_booking'),
   # path('profile/', views.user_profile, name='user_profile'),
    
    # Static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),'''