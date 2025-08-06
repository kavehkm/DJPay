# standard
from typing import Any

# internal
from ..models import Bill
from .base import BaseBackend


class Zibal(BaseBackend):
    """Zibal"""

    identifier = "zarinpal"
    label = "ZarinPal"

    @classmethod
    def validate_config(cls, config: dict) -> dict:
        # extract required data
        merchant_id = config.get("merchant_id")
        callback_view_name = config.get("callback_view_name")

        # validate merchant_id
        if not merchant_id or not isinstance(merchant_id, str):
            raise PaymentImproperlyConfiguredError("Invalid merchant_id.")
        # validate callback_view_name
        if not callback_view_name or not isinstance(callback_view_name, str):
            raise PaymentImproperlyConfiguredError("Invalid callback_view_name.")
        try:
            reverse(callback_view_name, {"bill_id": SAMPLE_BILL_ID})
        except NoReverseMatch:
            raise PaymentImproperlyConfiguredError("Invalid callback_view_name.")

        return config

    @property
    def merchant_id(self) -> str:
        return self._get_config("merchant_id")

    def pay(self, amount: int, **extra: Any) -> Bill:
        pass

    def verify(self, bill: Bill, **kwargs: Any) -> Bill:
        pass
