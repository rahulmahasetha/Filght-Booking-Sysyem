from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from home.models import Contact, Airport, Airline, Flight, Payment, Booking, Passenger, UserProfile, FlightRoute, RouteStop, Ticket, BookingSegment

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

class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 1
    sortable_field_name = "sequence"
    fields = ('sequence', 'airport', 'arrival_time', 'departure_time', 'departure_airline', 'flight_number')

@admin.register(FlightRoute)
class FlightRouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'stops_count', 'is_active')
    inlines = [RouteStopInline]
    def stops_count(self, obj):
        return obj.stops.count()

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'route', 'departure_time', 'stops', 'cabin_allowance', 'check_in_allowance', 'available_seats', 'dynamic_pricing_status')
    list_editable = ('cabin_allowance', 'check_in_allowance')
    search_fields = ('flight_number', 'airline__name', 'departure_airport__city', 'arrival_airport__city', 'cabin_allowance', 'check_in_allowance')
    list_filter = ('airline', 'departure_time', 'departure_airport')
    date_hierarchy = 'departure_time'
    fieldsets = (
        ('Flight Route', {
            'fields': ('flight_number', 'airline', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'stops')
        }),
        ('Seats & Prices', {
            'fields': ('economy_seats', 'business_seats', 'first_class_seats', 'economy_price', 'business_price', 'first_class_price')
        }),
        ('Cabin & Check-in Rules', {
            'fields': ('cabin_allowance', 'check_in_allowance')
        }),
    )
    def route(self, obj):
        return f"{obj.departure_airport.code} ✈ {obj.arrival_airport.code}"
    def available_seats(self, obj):
        total = obj.economy_seats + obj.business_seats + obj.first_class_seats
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', 'green' if total > 20 else 'red', total)
    def dynamic_pricing_status(self, obj):
        total = obj.economy_seats + obj.business_seats + obj.first_class_seats
        if total < 10: return format_html('<span style="color: red; font-weight: bold;">Surge</span>')
        elif total > 100: return format_html('<span style="color: green;">Discount</span>')
        return "Normal"

class BookingSegmentInline(admin.TabularInline):
    model = BookingSegment
    extra = 0

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference', 'user', 'travel_class', 'fare_type', 'nums_passengers', 'discount_amount', 'total_price', 'status_badge')
    search_fields = ('reference', 'user__username')
    list_filter = ('status', 'travel_class', 'fare_type', 'booking_date')
    inlines = [BookingSegmentInline]
    def status_badge(self, obj):
        colors = {'CONFIRMED': 'green', 'CANCELLED': 'red', 'PENDING': 'orange'}
        return format_html('<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 4px;">{}</span>', colors.get(obj.status, 'gray'), obj.status)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'passenger', 'airline_name', 'flight_number', 'issued_at')
    search_fields = ('ticket_number', 'passenger__first_name', 'flight_number')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'booking', 'amount', 'status')

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'booking', 'is_child')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
