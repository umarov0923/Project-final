import random
import uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from shared.models import BaseModel

# Create your models here.
SELLER, MANAGER, ADMIN = ('seller','manager', 'admin')

class User(AbstractUser, BaseModel):
    USER_ROLES= (
        (SELLER, SELLER),
        (MANAGER, MANAGER),
    )
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )
    user_roles= models.CharField(max_length=31, choices=USER_ROLES, default=SELLER)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions = ['jpg', 'jpeg', 'heic', 'heif'])])

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def check_username(self):
        if not self.username:
            temp_username = f'instagram-{uuid.uuid4().__str__().split("-")[-1]}'
            while User.objects.filter(username=temp_username).exists():
                temp_username = f'{temp_username}{random.randint(0,9)}'
            self.username = temp_username

    def check_email(self):
        if self.email:
            normalize_email = self.email.lower() #Mukarramboy@gmail.com -> mukarramboy@gmail.com
            self.email = normalize_email

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

    def clean(self):
        self.check_email()
        self.check_username()


    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)

