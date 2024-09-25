from django.db import models
from django.contrib.auth.models import User


class Crypto(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=20)
    ticker = models.CharField(blank=False, max_length=10)
    amount = models.FloatField(blank=False)

    def __str__(self) -> str:
        return f"{self.owner.id} {self.name}({self.ticker})"
    
    class Meta:
        verbose_name = 'Crypto'  # Исправлено


class Share(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=20)
    ticker = models.CharField(blank=False, max_length=10)
    amount = models.FloatField(blank=False, default=1)  # Поле с дефолтным значением

    def __str__(self) -> str:
        return f"{self.owner.id} {self.name}({self.ticker})"

    class Meta:
        verbose_name = 'Share'
        verbose_name_plural = 'Shares'  # Обычно во множественном числе