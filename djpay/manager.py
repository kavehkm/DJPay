# dj
from django.utils.functional import cached_property

# internal
from .backends.base import BaseBackend
from .errors import PaymentBackendDoesNotExistError


class PayManager(object):
    """PayManager"""

    @cached_property
    def backends(self) -> list:
        from .backends import BACKENDS

        return BACKENDS

    def get_backend(self, identifier: str, config: dict | None = None) -> BaseBackend:
        for backend in self.backends:
            if identifier == backend.identifier:
                return backend(config)
        raise PaymentBackendDoesNotExistError
