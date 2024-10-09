class BasePaymentError(Exception):
    """Base Payment Error"""


class PaymentError(BasePaymentError):
    """Payment Error"""


class PaymentBackendDoesNotExistError(BasePaymentError):
    """PaymentBackend Does Not Exist Error"""
