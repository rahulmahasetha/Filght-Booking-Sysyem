import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.test import Client, RequestFactory
from home.views import flight_search

factory = RequestFactory()
request = factory.post('/search/', {
    'departure': '1',
    'arrival': '2',
    'date': '2026-07-06',
    'passengers': '1',
    'class': 'ECONOMY',
    'fare_type': 'NORMAL'
})
# simulate Session and Messages middleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

middleware = SessionMiddleware(lambda r: None)
middleware.process_request(request)
request.session.save()
msg_middleware = MessageMiddleware(lambda r: None)
msg_middleware.process_request(request)

try:
    response = flight_search(request)
    print(f"Status code: {response.status_code}")
except Exception as e:
    import traceback
    traceback.print_exc()

