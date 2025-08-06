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
        return config

    def pay(self, amount: int, **extra: Any) -> Bill:
        pass

    def verify(self, bill: Bill, **kwargs: Any) -> Bill:
        pass
