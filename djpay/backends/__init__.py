# internal
from .pay_on_delivery import PayOnDelivery
from .zarinpal import ZarinPal


BACKENDS = [
    PayOnDelivery,
    ZarinPal,
]
