from django.conf import settings
import requests


def send_message_android(destination, title, message):
    headers = {
        'Authorization': 'key=' + settings.FIREBASE_SERVER_KEY,
        'Content - Type': 'application/json'
    }
    payload = {
        "to": destination,
        "notification": {"title": title, "text": message}
    }
    request = requests.post(
        settings.FIREBASE_API_URL,
        json=payload,
        headers=headers
    )
    print request.text