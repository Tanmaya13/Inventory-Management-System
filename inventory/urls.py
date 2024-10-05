from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from inventory.views import ItemCreateViewSet, ItemDetailsViewSet

PATTERNS = (
    [
        path('items/', ItemCreateViewSet.as_view(), name='item_creation'),
        path('items/<item_id>/', ItemDetailsViewSet.as_view(), name='item_details'),
        path('get_jwt_token/', TokenObtainPairView.as_view(), name='login'),
    ],
    "inventory",
    "inventory",
)

# super admin user --> tanmaya
# password --> admin