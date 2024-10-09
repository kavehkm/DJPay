#!/usr/bin/env python

# dj
from django.core.management import call_command

# internal
from boot_django import boot_django


# call the django setup routine
boot_django()

call_command("makemigrations", "djpay")
