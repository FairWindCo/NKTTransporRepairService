from django.db import models

# Create your models here.
from Counterparty.models import Partner

CONTACT_TYPES = (
    ('EM', 'E-MAIL'),
    ('PH', 'PHONE'),
    ('ST', 'SITE'),
    ('PR', 'PORTAL'),
    ('AD', 'ADDRESS'),
)


class ContactInfo(models.Model):
    contact_type = models.CharField(choices=CONTACT_TYPES, max_length=2, verbose_name='Тип')
    title = models.CharField(max_length=255, verbose_name='Контактное лицо', default=None)
    value = models.CharField(max_length=255, verbose_name='Контакт')
    additional_info = models.CharField(max_length=255, verbose_name='Дополнительные данные', default=None)
    partner = models.ForeignKey(Partner, null=True, default=None, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        db_table = 'contacts'
        indexes = [
            models.Index(fields=['contact_type']),
        ]

    def __str__(self):
        return f'{self.contact_type}: {self.value}'
