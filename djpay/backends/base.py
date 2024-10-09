# standard
from typing import Any

# internal
from ..models import Bill
from ..errors import PaymentError


class BaseBackend(object):
    """Base Backend"""

    identifier = "base"
    label = "Base"

    def __init__(self, config: dict | None = None) -> None:
        if config is None:
            config = {}
        self._config = self._validate_config(config)

    def _validate_config(self, config: dict) -> dict:  # noqa
        return config

    def _get_config(self, name: str, default: Any = None) -> Any:
        return self._config.get(name, default)

    def error(self, message: str) -> None:
        raise PaymentError(message)

    def pay(self, amount: int, **extra: Any) -> Bill:
        raise NotImplementedError

    def verify(self, bill_id: int, **kwargs: Any) -> Bill:
        raise NotImplementedError

    def __str__(self):
        return self.label

    def __repr__(self):
        return f"Backend(identifier={self.identifier}, label={self.label})"
