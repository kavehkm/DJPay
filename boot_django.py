# standard
import sys
from pathlib import Path

# dj
import django
from django.conf import settings


BASE_DIR = Path(__file__).parent / "djpay/"
sys.path.insert(0, str(BASE_DIR))


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR.parent / "djdjpay/db.sqlite3",
            }
        },
        INSTALLED_APPS=("djpay",),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()
