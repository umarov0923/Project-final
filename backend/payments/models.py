from shared.models import BaseModel
from debts.models import Debt
from django.db import models


class Payment(BaseModel):
    """Payments made by clients"""
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE, related_name="payments", verbose_name="Debt")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Payment Amount")
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="User",
    )

    def save(self, *args, **kwargs):
        if self.debt.remaining_amount >= self.amount:
            self.debt.remaining_amount -= self.amount
            self.debt.client.balanse -= self.amount
        else:
            raise ValueError("Payment exceeds remaining debt amount.")
        super().save(*args, **kwargs)
        self.debt.save()
        self.debt.client.save()

    def __str__(self):
        return f"Payment of {self.amount} for {self.debt.client.name}"
