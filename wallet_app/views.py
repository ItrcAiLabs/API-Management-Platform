from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Transaction, User
from .serializers import TransactionSerializer
from .forms import RegistrationForm, LoginForm
from zarinpal.api import ZarinPalPayment

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('wallet_view')
        return render(request, 'register.html', {'form': form})

class WalletAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        transactions = Transaction.objects.filter(user=user).order_by('-created_at')[:10]
        serialized_transactions = TransactionSerializer(transactions, many=True)
        return Response({
            'wallet_balance': user.wallet_balance,
            'transactions': serialized_transactions.data
        })

class RechargeWalletAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        if not amount or float(amount) <= 0:
            return Response({'error': 'Invalid amount'}, status=400)

        payment = ZarinPalPayment(settings.ZARINPAL_MERCHANT_ID, float(amount))
        callback_url = settings.ZARINPAL_CALLBACK_URL
        description = "Wallet recharge"

        result = payment.request_payment(callback_url, description, request.user.username, "user@example.com")
        if result['status'] == 'success':
            return Response({'payment_url': result['payment_url']})
        return Response({'error': 'Payment initiation failed'}, status=500)

class VerifyPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        authority = request.GET.get('Authority')
        if not authority:
            return Response({'error': 'No payment authority provided'}, status=400)

        payment = ZarinPalPayment(settings.ZARINPAL_MERCHANT_ID)
        verification_result = payment.verify_payment(authority)

        if verification_result['status'] == 'success':
            request.user.wallet_balance += verification_result['amount']
            request.user.save()

            Transaction.objects.create(
                user=request.user,
                amount=verification_result['amount'],
                description="Wallet recharge via ZarinPal"
            )
            return Response({'message': 'Payment verified and wallet recharged'})
        return Response({'error': 'Payment verification failed'}, status=500)
