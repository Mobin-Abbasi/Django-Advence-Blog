from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page

import requests

from .tasks import sendEmail


def send_email(request):
    sendEmail.delay()
    return HttpResponse("Done sending")


@cache_page(60)
def test(request):
    response = requests.get(
        "https://7cf46101-84b5-41ce-bc7b-74ae829f14ff.mock.pstmn.io/test/delay/5"
    )
    return JsonResponse(response.json())
