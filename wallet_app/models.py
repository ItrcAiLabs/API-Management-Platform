from django.contrib.auth.models import AbstractUser
from django.db import models
import redis

# Redis connection setup
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


class User(AbstractUser):
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        key = f'user:{self.user.id}:transactions'
        redis_client.lpush(key, self.pk) 
        redis_client.ltrim(key, 0, 9)  