# pharmacy/apps.py
from django.apps import AppConfig

class PharmacyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pharmacy"

    def ready(self):
        # 🔹 Seed initial data for Render Free (15 users, stores, medicines, inventory)
        try:
            from .seed_data import seed
            seed()
        except Exception:
            pass
