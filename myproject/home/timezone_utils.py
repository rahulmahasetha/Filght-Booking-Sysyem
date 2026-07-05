from datetime import datetime

from django.utils import timezone


def ensure_aware_datetime(value):
    if value is None:
        return None
    if timezone.is_aware(value):
        return value
    return timezone.make_aware(value, timezone.get_default_timezone())


def ensure_aware_datetime_from_string(value, fmt):
    parsed = datetime.strptime(value, fmt)
    return ensure_aware_datetime(parsed)
