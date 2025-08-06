# standard
from typing import Any

# requests
import requests

# dj
from django.urls import reverse
from django.http import HttpRequest
from django.urls.exceptions import NoReverseMatch

# internal
from ..models import Bill
from .base import BaseBackend
from ..utils import absolute_reverse
from ..errors import PaymentImproperlyConfiguredError


SAMPLE_BILL_ID = 0
SUCCESS_STATUS_CODE = 100
PAY_ENDPOINT = "https://gateway.zibal.ir/start/"
VERIFY_ENDPOINT = "https://gateway.zibal.ir/v1/verify"
INITIAL_ENDPOINT = "https://gateway.zibal.ir/v1/request"


class Zibal(BaseBackend):
    """Zibal"""

    identifier = "zibal"
    label = "Zibal"

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

    def get_callback_url(self, bill_id: int, request: HttpRequest = None) -> str:
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
        # pop out request from extra
        request = extra.pop("request", None)

        # get optional data from extra
        description = extra.get("description")
        order_id = extra.get("order_pk")
        mobile = extra.get("mobile")

        # create bill
        bill = Bill.objects.create(
            backend=self.identifier,
            amount=amount,
            extra=extra,
        )

        # send initialize request
        data = {
            "merchant": self.merchant_id,
            "amount": amount,
            "callbackUrl": self.get_callback_url(bill.id, request),
            "description": description,
            "orderId": order_id,
            "mobile": mobile,
        }
        res = requests.post(INITIAL_ENDPOINT, data=data).json()

        # check for errors
        if res["result"] != SUCCESS_STATUS_CODE:
            self.error(res["message"])

        # there is no error and invalid-code so:
        # add redirect-url as next_step on bill instance
        # and return it as response
        bill.next_step = PAY_ENDPOINT + res["trackId"]
        bill.save(update_fields=["next_step"])
        return bill

    def verify(self, bill: Bill, **kwargs: Any) -> Bill:
        # check for backend
        if bill.backend != self.identifier:
            self.error("Invalid bill.")
        # check verified status
        if bill.verified:
            self.error("Invalid bill.")
        # check for track_id in kwargs
        if "trackId" not in kwargs:
            self.error("Required trackId parameter not provided.")

        # send verify request
        data = {
            "merchant": self.merchant_id,
            "trackId": kwargs["trackId"],
        }
        res = requests.post(VERIFY_ENDPOINT, data=data).json()

        # check for errors
        if res["result"]  != SUCCESS_STATUS_CODE:
            self.error(res["message"])

        # there is no error and invalid-code so:
        # 1) add refNumber as transaction_id on bill instance
        # 2) change verified status value to True
        # 3) save zibal verify response to extra field
        # and return it as response
        bill.transaction_id = res["refNumber"]
        bill.verified = True
        bill.extra["verify_response"] = res
        bill.save(update_fields=["transaction_id", "verified", "extra"])
        return bill
