"""Push notification service

send_message_android and send_message_ios are the same, but this is intentional, in order
to support any future different conditions for both platforms, different keys or addtional parameters
shit happens sometimes ROFL!

"""

from django.conf import settings
from constance import config
import requests


def send_message_android(destination, message, title=config.TITLE_PUSH_NOTIFICATION):
    headers = {
        'Authorization': 'key=' + settings.FIREBASE_SERVER_KEY,
        'Content - Type': 'application/json'
    }
    payload = {
        "to": destination,
        "data": {
            "title": title,
            "detail": message
        }
    }
    request = requests.post(
        settings.FIREBASE_API_URL,
        json=payload,
        headers=headers
    )
    print request.text


def send_message_ios(destination, message, title=config.TITLE_PUSH_NOTIFICATION):
    headers = {
        'Authorization': 'key=' + settings.FIREBASE_SERVER_KEY,
        'Content - Type': 'application/json'
    }
    payload = {
        "to": destination,
        "priority": "high",
        "sound": "default",
        "badge": 1,
        "data": {
            "title": title,
            "detail": message
        }
    }
    request = requests.post(
        settings.FIREBASE_API_URL,
        json=payload,
        headers=headers
    )
    print request.text


def send_push_notification(user, message):
    try:
        devices = user.employeedevice_set.all()
        if devices[0].android_device:
            send_message_android(devices[0].android_device, message)
        if devices[0].ios_device:
            send_message_ios(devices[0].ios_device, message)
        return True
    except:
        return False