import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.test import Client, RequestFactory
from django.contrib.auth import get_user_model
from home.views import book_flight

User = get_user_model()
user = User.objects.first()

factory = RequestFactory()
request = factory.get('/book/1/?passengers=1&class=ECONOMY&fare_type=NORMAL&path=1')
request.user = user

from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

middleware = SessionMiddleware(lambda r: None)
middleware.process_request(request)
request.session.save()
msg_middleware = MessageMiddleware(lambda r: None)
msg_middleware.process_request(request)

try:
    response = book_flight(request, 1)
    print(f"Status code: {response.status_code}")
except Exception as e:
    import traceback
    traceback.print_exc()

