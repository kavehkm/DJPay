# standard
from typing import Any

# internal
from .base import BaseBackend
from ..models import Bill


class PayOnDelivery(BaseBackend):
    """Pay On Delivery"""

    identifier = "pay-on-delivery"
    label = "Pay on delivery"

    def pay(self, amount: int, **extra: Any) -> Bill:
        return Bill.objects.create(backend=self.identifier, amount=amount, extra=extra)

    def verify(self, bill: Bill) -> Bill:
        return super().verify(bill)
