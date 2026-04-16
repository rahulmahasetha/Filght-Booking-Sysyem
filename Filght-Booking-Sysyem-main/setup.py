from setuptools import setup, find_packages

setup(
    name='filght-booking-system',
    version='1.0.0',
    description='Flight Booking System Django Application',
    python_requires='>=3.12',
    packages=find_packages(),
    install_requires=[
        'Django==5.1.7',
        'mysqlclient==2.2.0',
        'stripe==9.13.0',
        'python-decouple==3.8',
        'whitenoise==6.6.0',
        'gunicorn==21.2.0',
    ],
)
