from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from home.models import Contact, Airport, Airline, Flight, Payment, Booking, Passenger, UserProfile

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'country')
    search_fields = ('code', 'name', 'city', 'country')
    list_filter = ('country',)

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'logo_preview')
    search_fields = ('code', 'name')
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="40" style="border-radius:4px;" />', obj.logo.url)
        return "-"
    logo_preview.short_description = "Logo"

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'route', 'departure_time', 'available_seats', 'dynamic_pricing_status')
    search_fields = ('flight_number', 'airline__name', 'departure_airport__city', 'arrival_airport__city')
    list_filter = ('airline', 'departure_time', 'departure_airport')
    date_hierarchy = 'departure_time'
    
    def route(self, obj):
        return f"{obj.departure_airport.code} ✈ {obj.arrival_airport.code}"
    
    def available_seats(self, obj):
        total = obj.economy_seats + obj.business_seats + obj.first_class_seats
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', 'green' if total > 20 else 'red', total)

    def dynamic_pricing_status(self, obj):
        total = obj.economy_seats + obj.business_seats + obj.first_class_seats
        if total < 10:
            return format_html('<span style="color: red; font-weight: bold;">Surge (High Demand)</span>')
        elif total > 100:
            return format_html('<span style="color: green;">Discount Active</span>')
        return "Normal"

class PassengerInline(admin.TabularInline):
    model = Passenger
    extra = 0

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference', 'user', 'flight', 'travel_class', 'nums_passengers', 'total_price', 'status_badge')
    search_fields = ('reference', 'user__username', 'flight__flight_number')
    list_filter = ('status', 'travel_class', 'booking_date')
    date_hierarchy = 'booking_date'
    inlines = [PassengerInline]
    actions = ['mark_confirmed', 'mark_cancelled']

    def status_badge(self, obj):
        colors = {'CONFIRMED': 'green', 'CANCELLED': 'red', 'PENDING': 'orange'}
        return format_html('<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold;">{}</span>', colors.get(obj.status, 'gray'), obj.status)
    status_badge.short_description = "Status"

    def mark_confirmed(self, request, queryset):
        queryset.update(status='CONFIRMED')
    mark_confirmed.short_description = "Mark selected bookings as Confirmed"

    def mark_cancelled(self, request, queryset):
        queryset.update(status='CANCELLED')
    mark_cancelled.short_description = "Mark selected bookings as Cancelled"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'booking', 'amount', 'payment_date', 'status')
    search_fields = ('transaction_id', 'booking__reference')
    list_filter = ('status', 'payment_date')
    date_hierarchy = 'payment_date'

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'booking', 'id_type', 'id_number')
    search_fields = ('first_name', 'last_name', 'id_number', 'booking__reference')
    list_filter = ('id_type',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date')
    search_fields = ('name', 'email')
    list_filter = ('date',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'gender', 'dob')
    search_fields = ('user__username', 'phone')
    list_filter = ('gender',)
