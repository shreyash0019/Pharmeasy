from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from pharmacy.views import (
    MedicineViewSet,
    MedicalStoreViewSet,
    StoreInventoryViewSet,
    search_medicine
)

from orders.views import OrderViewSet
from reminders.views import ReminderViewSet
from accounts.views import RegisterView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('medicines', MedicineViewSet)
router.register('stores', MedicalStoreViewSet)
router.register('inventory', StoreInventoryViewSet)
router.register('orders', OrderViewSet)
router.register('reminders', ReminderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('api/register/', RegisterView.as_view()),
    path('api/login/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # Search
    path('api/search/', search_medicine),

    # All ViewSets
    path('api/', include(router.urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)