import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings

# Initialize Firebase (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)


def send_fcm_notification(token, title, body):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )

        response = messaging.send(message)
        print("FCM Success:", response)
        return response

    except Exception as e:
        print("FCM Error:", str(e))
        return None
