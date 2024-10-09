# dj
from django.urls import reverse
from django.http.request import HttpRequest


def absolute_reverse(
    request: HttpRequest,
    view: str,
    args: list | None = None,
    kwargs: dict | None = None,
) -> str:
    return request.build_absolute_uri(reverse(view, args=args, kwargs=kwargs)).replace(
        "127.0.0.1", "localhost"
    )
