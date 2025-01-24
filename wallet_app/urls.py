from django.urls import path
from .views import RegisterView, WalletAPIView, RechargeWalletAPIView, VerifyPaymentAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('api/wallet/', WalletAPIView.as_view(), name='api_wallet'),
    path('api/recharge/', RechargeWalletAPIView.as_view(), name='api_recharge'),
    path('api/verify/', VerifyPaymentAPIView.as_view(), name='api_verify'),
]
