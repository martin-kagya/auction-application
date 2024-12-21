from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserInfo,
    UserRegistrationView,
    UserLoginView,
    ItemViewSet,
    BidViewSet,
    AuctionViewSet,
    WatchlistViewSet,
    PaymentViewSet,
)

# Create a router and register your viewsets
router = DefaultRouter()
router.register('user-info', UserInfo, basename='user-info')
router.register('items', ItemViewSet, basename='items')
router.register('bids', BidViewSet, basename='bids')
router.register('auctions', AuctionViewSet, basename='auctions')
router.register('watchlist', WatchlistViewSet, basename='watchlist')
router.register('payments', PaymentViewSet, basename='payments')

urlpatterns = [
    # Authentication and registration endpoints
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),

    # Include router URLs for viewsets
    path('', include(router.urls)),
]
