import json

from django.http import HttpResponse


def index(request):
    return HttpResponse("Welcome to kaseb tracking report")


def ping(request):
    response_data = dict(
        message="pong"
    )
    return HttpResponse(json.dumps(response_data), content_type="application/json")
