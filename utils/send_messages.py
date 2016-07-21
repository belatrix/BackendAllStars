"""Push notification service

send_message_android and send_message_ios are similar, but this is intentional, in order
to support any future different conditions for both platforms, different keys or addtional parameters
shit happens sometimes ROFL!

"""

from django.conf import settings
from constance import config
import requests


def send_message_android(destination, message):
    headers = {
        'Authorization': 'key=' + settings.FIREBASE_SERVER_KEY,
        'Content - Type': 'application/json'
    }
    payload = {
        "to": destination,
        "data": {
            "title": config.TITLE_PUSH_NOTIFICATION,
            "detail": message
        }
    }
    request = requests.post(
        settings.FIREBASE_API_URL,
        json=payload,
        headers=headers
    )
    print request.text


def send_message_ios(destination, message):
    headers = {
        'Authorization': 'key=' + settings.FIREBASE_SERVER_KEY,
        'Content - Type': 'application/json'
    }
    payload = {
        "to": destination,
        "priority": "high",
        "badge": 0,
        "notification": {
            "title": config.TITLE_PUSH_NOTIFICATION,
            "text": message,
            "sound": "default",
        }
    }
    request = requests.post(
        settings.FIREBASE_API_URL,
        json=payload,
        headers=headers
    )
    print request.text


def send_push_notification(to_user, message):
    try:
        devices = to_user.employeedevice_set.all()
        if devices[0].android_device:
            send_message_android(devices[0].android_device, message)
        if devices[0].ios_device:
            send_message_ios(devices[0].ios_device, message)
        return True
    except:
        return False


def evaluate_user_permissions_for_push(user):
    roles = user.role.all()
    for role in roles:
        if config.ROLE_AUTHORIZED == role.name:
            return True
