from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from pharmacy.views import (
    MedicineViewSet,
    MedicalStoreViewSet,
    StoreInventoryViewSet,
    search_medicine,
    get_stores,
    get_orders,
    get_reminders
)

from orders.views import OrderViewSet
from reminders.views import ReminderViewSet
from accounts.views import RegisterView, CustomLoginView

from rest_framework_simplejwt.views import TokenRefreshView


# 🔹 Router
router = DefaultRouter()
router.register('medicines', MedicineViewSet)
router.register('stores', MedicalStoreViewSet)  # queryset added in views.py
router.register('inventory', StoreInventoryViewSet)  # queryset added in views.py
router.register('orders', OrderViewSet)
router.register('reminders', ReminderViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔐 Auth
    path('api/register/', RegisterView.as_view()),
    path('api/login/', CustomLoginView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # 🔍 Search
    path('api/search/', search_medicine),

    # ✅ Custom APIs
    path('api/stores/all/', get_stores),
    path('api/orders/my/', get_orders),
    path('api/reminders/my/', get_reminders),

    # 🔹 ViewSets
    path('api/', include(router.urls)),
]

# 📁 Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
