from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from clients.models import Client

def default_due_date():
    return now().date() + timedelta(days=30)

class Debt(models.Model):
    """Задолженности клиентов"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="debts", verbose_name="Клиент")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма долга")
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Остаток долга")
    due_date = models.DateField(verbose_name="Срок оплаты", default=default_due_date)
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")

    def save(self, *args, **kwargs):
        """Автоматически заполняет остаток долга и отмечает оплату"""
        if not self.id:  # Если создается новый объект
            self.remaining_amount = self.total_amount
            self.client.balanse += self.total_amount
            self.client.save()
        if self.remaining_amount == 0:
            self.is_paid = True 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.name} - {self.remaining_amount} руб."
