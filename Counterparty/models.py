from django.db import models

# Create your models here.
from django.db.models import UniqueConstraint


class Partner(models.Model):
    name = models.CharField("Название", max_length=190)
    full_name = models.CharField("Полное имя", max_length=250, blank=True, null=True, default=None)
    alt_name = models.CharField("Дополнительное имя", max_length=250, blank=True, null=True, default=None)
    code = models.CharField("1C Код", max_length=15, blank=True, null=True, default=None)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, default=None)
    is_customer = models.BooleanField('Может быть покупателем', default=False)
    is_seller = models.BooleanField('Модет быть продавцом', default=False)
    is_service = models.BooleanField('Может принимать в сервис', default=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        db_table = 'partner'
        ordering = ['name']
        constraints = [
            UniqueConstraint(fields=['name'], name='u_partner_name'),
            UniqueConstraint(fields=['code'], name='u_partner_code'),
        ]