from rest_framework import serializers
from .models import Transaction, User


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'created_at']

class WalletSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['wallet_balance', 'transactions']