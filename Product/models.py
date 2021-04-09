import logging
import re

from django.db import models

# Create your models here.
from django.db.models import UniqueConstraint

logger = logging.getLogger(__name__)

class Currencies(models.Model):
    name = models.CharField("Сurrency Name", max_length=50)
    code = models.CharField("Code", max_length=3, blank=True, null=True, default=None)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
        db_table = 'trade_сurrency'
        ordering = ['name']
        constraints = [
            UniqueConstraint(fields=['name'], name='u_trade_сur'),
            UniqueConstraint(fields=['code'], name='u_trade_сur_code'),
        ]


class Categories(models.Model):
    name = models.CharField("Category Name", max_length=150)
    code = models.CharField("1C Code", max_length=15, blank=True, null=True, default=None)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL,
                               blank=True, null=True, )

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'trade_category'
        ordering = ['name']
        constraints = [
            UniqueConstraint(fields=['name', 'parent', 'code'], name='u_trade_cat'),
            UniqueConstraint(fields=['code'], name='u_trade_cat_code'),
        ]


class Brands(models.Model):
    name = models.CharField("Brand Name", max_length=150)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        db_table = 'trade_brands'
        ordering = ['name']
        constraints = [
            UniqueConstraint(fields=['name'], name='u_trade_brand')
        ]


VENDOR_SIMPLIFY = re.compile(r'[\s._@#№*+\/\\\-]+')


def simplify_vendor_code(vendor_code: str):
    result = None
    if vendor_code:
        try:
            result = VENDOR_SIMPLIFY.sub('', vendor_code).upper()
        except Exception as e:
            logger.error('SIMPLE CODE FOR {} ERROR {}'.format(vendor_code, e))
            result = None
    return result


class Products(models.Model):
    name = models.CharField("Product Name", max_length=190)
    code = models.CharField("1C Code", max_length=15, blank=True, null=True, default=None)
    vendor_code = models.CharField("Vendor Code", max_length=60, blank=True, null=True, default=None)
    product_code = models.CharField("Product Code", max_length=60, blank=True, null=True, default=None)
    bar_code = models.CharField("Bar Code", max_length=20, blank=True, null=True, default=None)
    brand = models.ForeignKey(Brands, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    default_warranty = models.IntegerField("Default Warranty", blank=True, null=True, default=None)
    default_price = models.DecimalField("Default Price", blank=True, null=True, default=None,
                                        max_digits=10, decimal_places=3)
    currency = models.ForeignKey(Currencies, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    categories = models.ManyToManyField(Categories, blank=True)
    is_service = models.BooleanField('Service', default=False)
    search_code = models.CharField("Code for Search", max_length=60, blank=True, null=True, default=None)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.search_code = simplify_vendor_code(self.vendor_code)
        super().save(force_insert, force_update, using, update_fields)

    @property
    def vendor_code_simplify(self):
        return simplify_vendor_code(self.vendor_code)

    def __str__(self):
        return '{} {}'.format(self.brand.name if self.brand else '', self.name)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        db_table = 'trade_products'
        ordering = ['name']
        constraints = [
            UniqueConstraint(fields=['code'], name='u_trade_prod_code'),
            UniqueConstraint(fields=['name', 'brand', 'code'], name='u_trade_prod_name')
        ]
        indexes = [
            models.Index(fields=['vendor_code']),
            models.Index(fields=['product_code']),
            models.Index(fields=['bar_code']),
        ]
