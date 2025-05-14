from django.db import models
from shared.models import BaseModel


class Client(BaseModel):
    """Модель клиента магазина"""
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20,)
    balanse = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='clients',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'name'],
                name='unique_client_name_per_company'
            ),
            models.UniqueConstraint(
                fields=['company', 'phone'],
                name='unique_client_phone_per_company'
            )
        ]