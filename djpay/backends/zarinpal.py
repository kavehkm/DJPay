# standard
from typing import Any

# requests
import requests

# dj
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured

# internal
from ..models import Bill
from .base import BaseBackend
from ..errors import PaymentError
from ..utils import absolute_reverse


SUCCESS_STATUS_CODE = 100
PAY_ENDPOINT = "https://www.zarinpal.com/pg/StartPay/"
VERIFY_ENDPOINT = "https://api.zarinpal.com/pg/v4/payment/verify.json"
INITIAL_ENDPOINT = "https://api.zarinpal.com/pg/v4/payment/request.json"


class ZarinPal(BaseBackend):
    """ZarinPal"""

    identifier = "zarinpal"
    label = "ZarinPal"

    def _validate_config(self, config: dict) -> dict:
        # extract required data
        currency = config.get("currency")
        merchant_id = config.get("merchant_id")
        callback_view_name = config.get("callback_view_name")

        # validate currency
        if (
            not currency
            or not isinstance(currency, str)
            or currency not in ["IRT", "IRR"]
        ):
            raise ImproperlyConfigured("Invalid currency.")
        # validate merchant_id
        if not merchant_id or not isinstance(merchant_id, str):
            raise ImproperlyConfigured("Invalid merchant_id")
        # validate callback_view_name
        if not callback_view_name or not isinstance(callback_view_name, str):
            raise ImproperlyConfigured("Invalid callback_view_name")

        return config

    @property
    def currency(self) -> str:
        return self._get_config("currency", "IRT")

    @property
    def merchant_id(self) -> str:
        return self._get_config("merchant_id")

    def get_callback_url(self, bill_id: int) -> str:
        request = self._get_config("request")
        callback_view_name = self._get_config("callback_view_name")
        callback_view_kwargs = {"bill_pk": bill_id}
        # check for request:
        # if request is present, its means user needs to absolute url
        # otherwise there is no need to absolute and relative is also acceptable
        if request:
            return absolute_reverse(
                request, callback_view_name, kwargs=callback_view_kwargs
            )
        else:
            return reverse(callback_view_name, kwargs=callback_view_kwargs)

    def pay(self, amount: int, **extra: Any) -> Bill:
        # create bill
        bill = Bill.objects.create(
            backend=self.identifier,
            amount=amount,
            extra=extra,
        )
        # send initialize request
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "currency": self.currency,
            "callback_url": self.get_callback_url(bill.id),
            "description": "No description provided.",
        }
        res = requests.post(INITIAL_ENDPOINT, data=data).json()
        # extract data and errors from response
        res_data = res.get("data")
        res_errors = res.get("errors")
        # check for errors
        if res_errors:
            raise PaymentError(res_errors.get("message"))
        # check for invalid code
        if res_data.get("code") != SUCCESS_STATUS_CODE:
            raise PaymentError("Invalid code.")
        # there is no error and invalid-code so:
        # add redirect-url as next_step on bill instance
        # and return it as response
        bill.next_step = PAY_ENDPOINT + res_data["authority"]
        bill.save(update_fields=["next_step"])
        return bill

    def verify(self, bill_id: int, **kwargs: Any) -> Bill:
        # check for Authority in kwargs
        if "Authority" not in kwargs:
            raise PaymentError("Required Authority parameter not provided.")
        # try to find bill by given id
        # just add transaction_id=None into conditions to ensure:
        # bill did not verify before
        try:
            bill = Bill.objects.get(id=bill_id, transaction_id=None)
        except Bill.DoesNotExist:
            raise PaymentError("Bill does not exist.")
        # send verify request
        data = {
            "authority": kwargs["Authority"],
            "amount": bill.amount,
            "merchant_id": self.merchant_id,
        }
        res = requests.post(VERIFY_ENDPOINT, data=data).json()
        # extract data and errors from response
        res_data = res.get("data")
        res_errors = res.get("errors")
        # check for errors
        if res_errors:
            raise PaymentError(res_errors.get("message"))
        # check for invalid code
        if res_data.get("code") != SUCCESS_STATUS_CODE:
            raise PaymentError("Invalid code.")
        # there is no error and invalid-code so:
        # add ref_id as transaction_id on bill instance
        # and return it as response
        bill.transaction_id = res_data["ref_id"]
        bill.save(update_fields=["transaction_id"])
        return bill
