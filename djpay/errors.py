class BasePaymentError(Exception):
    """Base Payment Error"""


class PaymentError(BasePaymentError):
    """Payment Error"""


class PaymentMethodDoesNotExist(BasePaymentError):
    """PaymentMethod Does Not Exist Error"""
