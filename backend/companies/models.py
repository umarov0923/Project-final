from django.db import models
from shared.models import BaseModel

# Create your models here.

class Company(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
