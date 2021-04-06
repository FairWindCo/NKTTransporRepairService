from django.contrib.auth.models import User
from django.db import models

from Counterparty.models import Partner
from Product.models import Products


# Create your models here.
class Breakdown(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, db_index=True, verbose_name='Поломка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поломка'
        verbose_name_plural = 'Поломки'
        ordering = ['name']


class Equipment(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, db_index=True, verbose_name='Поломка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комплектация'
        verbose_name_plural = 'Комплектация'
        ordering = ['name']


class ServiceStatuses(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, db_index=True, verbose_name='Название состояния')
    next_state = models.ManyToManyField('ServiceStatuses', default=None, verbose_name='Следующие действия', blank=True)
    is_start = models.BooleanField(default=False, verbose_name='Начальный этап')
    is_terminate = models.BooleanField(default=False, verbose_name='Завершает обработку')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Состояние заказа'
        verbose_name_plural = 'Состояния заказов'
        ordering = ['name']


class ServiceOrder(models.Model):
    created = models.DateTimeField("Created", auto_created=True)
    closed = models.DateTimeField("Closed", default=None, null=True, blank=True)
    state = models.ForeignKey(on_delete=models.CASCADE, to=ServiceStatuses)
    client = models.ForeignKey(on_delete=models.CASCADE, to=Partner, default=None, blank=True, null=True)
    parentOrder = models.ForeignKey("ServiceOrder", on_delete=models.SET_NULL, blank=True, null=True,
                                    verbose_name='На основании')
    modify_by = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Последний редактор',
                                  null=True, blank=True, related_name='modifiers')
    date_of_modify = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    comments = models.TextField(max_length=1000, blank=True, default='', verbose_name='Коментарий')

    class Meta:
        verbose_name = 'Сервисное обращение'
        verbose_name_plural = 'Сервисные обращения'
        ordering = ['created']


class ServiceProducts(models.Model):
    product = models.ForeignKey(on_delete=models.CASCADE, to=Products)
    serial_number = models.CharField("serial numbers", max_length=150, null=True, blank=True)
    date_of_sold = models.DateTimeField("sold", default=None, null=True, blank=True)
    life = models.PositiveIntegerField('life')
    date_of_purchase = models.DateTimeField("sold", default=None, null=True, blank=True)
    answerable = models.ForeignKey(on_delete=models.CASCADE, to=Partner, default=None, blank=True, null=True,
                                   related_name='responsibles')
    seller = models.ForeignKey(on_delete=models.CASCADE, to=Partner, default=None, blank=True, null=True,
                               related_name='sellers')
    buyer = models.ForeignKey(on_delete=models.CASCADE, to=Partner, default=None, blank=True, null=True,
                              related_name='buyers')
    sold_document = models.CharField("sold document", max_length=20, null=True, blank=True)
    purchase_document = models.CharField("purchase document", max_length=30, null=True, blank=True)
    warranty_document = models.CharField("warranty document", max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} [{self.product.product_code}] сн:{self.serial_number}"

    class Meta:
        verbose_name = 'Гарантийный товар'
        verbose_name_plural = 'Гарантийные товары'
        ordering = ['date_of_sold']


class ServiceOrderItem(models.Model):
    order = models.ForeignKey('Заказ на сервис', on_delete=models.CASCADE, to=ServiceOrder)
    service_product = models.ForeignKey('Изделие', on_delete=models.CASCADE, to=ServiceProducts)
    place = models.ForeignKey('Текущее местополодение', on_delete=models.CASCADE, to=Partner, default=None, blank=True,
                              null=True,
                              related_name='from_service')
    next_place = models.ForeignKey('Направляется', on_delete=models.CASCADE, to=Partner, default=None, blank=True,
                                   null=True,
                                   related_name='to_service')
    equipment = models.ManyToManyField('Комплектация', Equipment, on_delete=models.PROTECT)
    breakdown = models.ManyToManyField('Поломки', on_delete=models.PROTECT)
    replacement_product = models.ForeignKey('Замена на время ремона', on_delete=models.CASCADE, to=ServiceProducts,
                                            default=None, blank=True)
    reinforcement_product = models.ForeignKey('Замена на изделие', on_delete=models.CASCADE, to=ServiceProducts,
                                              default=None, blank=True)
    comments = models.TextField('Коментарий', max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.service_product}"


class OrderItemHistory(models.Model):
    order_item = models.ForeignKey(on_delete=models.CASCADE, to=ServiceOrderItem)
    comments = models.TextField(max_length=1000)
    date_of_change = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    place = models.ForeignKey(on_delete=models.CASCADE, to=Partner, default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.order_item} - {self.comments}"
