"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include


admin.site.site_header = "Uddan Admin"
admin.site.site_title = "FLIGHT BOOKING"
admin.site.index_title = "Welcome to Uddan"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.url'))
]


class MyModelAdmin(admin.ModelAdmin):
    # Display specific fields in the list view
    list_display = ('field1', 'field2', 'field3')

    # Add filters to the right sidebar
    list_filter = ('field1', 'field2')

    # Add search functionality
    search_fields = ('field1', 'field2')

    # Enable editing directly from the list view
    list_editable = ('field3',)

    # Add pagination
    list_per_page = 20

    # Customize the detail view
    fieldsets = (
        ('Section 1', {
            'fields': ('field1', 'field2')
        }),
        ('Section 2', {
            'fields': ('field3',),
            'classes': ('collapse',)  # Collapsible section
        }),
    )

