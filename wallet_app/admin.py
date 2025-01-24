from django.contrib import admin
from .models import User, Transaction

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'wallet_balance')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'created_at', 'description')
    search_fields = ('user__username', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
