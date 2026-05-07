from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES= (
        ("Vendedor,", "Vendedor"),
        ("Comprador", "Comprador"),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    phone = models.CharField(max_length=20, blank=True, null=True)
    
    
    
class seller  