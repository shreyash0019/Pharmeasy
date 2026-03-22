import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
import threading

# Initialize Firebase (run once)
if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)

def send_fcm_notification(token, title, body):
    def _send():
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                token=token,
            )
            messaging.send(message)
        except Exception as e:
            print("FCM error:", e)

    # run in background thread so API response is immediate
    threading.Thread(target=_send).start()
