# Generated by Django 3.2 on 2021-04-07 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='categories',
            name='u_trade_cat',
        ),
        migrations.RemoveConstraint(
            model_name='products',
            name='u_trade_prod_name',
        ),
        migrations.AddConstraint(
            model_name='categories',
            constraint=models.UniqueConstraint(fields=('name', 'parent', 'code'), name='u_trade_cat'),
        ),
        migrations.AddConstraint(
            model_name='products',
            constraint=models.UniqueConstraint(fields=('name', 'brand', 'code'), name='u_trade_prod_name'),
        ),
    ]
