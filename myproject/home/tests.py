from datetime import datetime

from django.test import SimpleTestCase
from django.utils import timezone

from .timezone_utils import ensure_aware_datetime


class TimezoneUtilsTests(SimpleTestCase):
    def test_ensure_aware_datetime_makes_naive_values_aware(self):
        naive_dt = datetime(2026, 5, 15, 18, 13, 50)

        aware_dt = ensure_aware_datetime(naive_dt)

        self.assertTrue(timezone.is_aware(aware_dt))
        self.assertEqual(aware_dt.year, 2026)
        self.assertEqual(aware_dt.month, 5)
        self.assertEqual(aware_dt.day, 15)
