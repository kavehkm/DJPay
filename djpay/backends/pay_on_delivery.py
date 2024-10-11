# standard
from typing import Any

# internal
from ..models import Bill
from .base import BaseBackend
from ..errors import PaymentError


class PayOnDelivery(BaseBackend):
    """Pay On Delivery"""

    identifier = "pay-on-delivery"
    label = "Pay on delivery"

    def pay(self, amount: int, **extra: Any) -> Bill:
        return Bill.objects.create(backend=self.identifier, amount=amount, extra=extra)

    def verify(self, bill_id: int, **kwargs: Any) -> Bill:
        # try to find bill by given id
        try:
            bill = Bill.objects.get(id=bill_id)
        except Bill.DoesNotExist:
            raise PaymentError("Bill does not exist.")
        # check verified status
        if bill.verified:
            raise PaymentError("Invalid bill.")
        # verify and return bill
        bill.verified = True
        bill.save(update_fields=["verified"])
        return bill
