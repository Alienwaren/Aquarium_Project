from plistlib import Dict

from aquarium_django.helpers.api import write_data_and_log
from aquarium_django.helpers.url import generate_json_response
from monitor.models import ApiKey, Habitat
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

data_topics = {
    "temperature": float,
     "insolation": float
}


def add_data_from_url(request, api_key: str, data_topic: str, value: str) -> JsonResponse:
    api_key_object = ApiKey.objects.filter(api_key=api_key).select_related().first()
    if api_key_object is None:
        json_response_str = generate_json_response(2, "Provided API key does not exist.", f"Following API: {api_key} key"
                                                                                          "does not exist.")
        return JsonResponse(json_response_str)

    habitat = api_key_object.habitat_owner
    if habitat is None:
        json_response_str = generate_json_response(1, "Habitat does not exist.", f"Following API: {api_key} key is not"
                                                                                 "assigned to any habitat.")
        return JsonResponse(json_response_str)

    if data_topic not in data_topics:
        json_response_str = generate_json_response(1, "Invalid data topic.", f"Following data topic: {data_topic} is invalid."
                                                                             f" Allowed topics: {list(data_topics.keys())}")
        return JsonResponse(json_response_str)

    try:
        data_topic_type = data_topics[data_topic]
        converted_value = data_topic_type(value)
        write_data_and_log(converted_value, habitat, data_topic)
        json_response_str = generate_json_response(0, "Data written successfully.")
        return JsonResponse(json_response_str)
    except ValueError:
        json_response_str = generate_json_response(4, "Incorrect data added.", f"Following data entry: {value} is invalid."
                                                                                f"It should be an float or integer value")
        return JsonResponse(json_response_str)