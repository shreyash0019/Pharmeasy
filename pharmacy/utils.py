import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
import threading


# ✅ Safe Firebase init (only when needed)
def initialize_firebase():
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print("Firebase init error:", e)


def send_fcm_notification(token, title, body):
    def _send():
        try:
            initialize_firebase()  # ✅ init here (not at import time)

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

    # ✅ run in background thread (non-blocking)
    threading.Thread(target=_send).start()
