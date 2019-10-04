from typing import Dict

from django.http import HttpResponse
from django.shortcuts import render
import json
import monitor_api.models as api_model

# Create your views here.
from aquarium_django.helpers.url import generate_json_response


def index_api(request):
    return HttpResponse("Hello, world. You're at the api index.")


def device_list(request) -> HttpResponse:
    """
    Method for listing paired devices with platform.
    :param request: HTTP request.
    :return HttpResponse: Response sent to browser - json containing registered devices
    """
    devices = api_model.Device.objects
    json_obj = {'devices': {}}
    for device in devices.all():
        json_obj['devices'].update({device.id: device.device_name})

    return HttpResponse(json.dumps(json_obj))

def add_new_device(request, device_name: str) -> Dict:
    if not device_name:
        return generate_json_response(-1, "Device name cannot be empty", {})