# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 18:19
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import drop.util.fields
import jsonfield.fields
import lablackey.unrest


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
            bases=(models.Model, lablackey.unrest.JsonMixin),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('extra', jsonfield.fields.JSONField(default=dict)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='drop.Cart')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Cart item',
                'verbose_name_plural': 'Cart items',
            },
            bases=(models.Model, lablackey.unrest.JsonMixin),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('order', models.FloatField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drop.Category')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, lablackey.unrest.JsonMixin),
        ),
        migrations.CreateModel(
            name='ExtraOrderItemPriceField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('value', drop.util.fields.CurrencyField(decimal_places=2, default=Decimal('0.0'), max_digits=30, verbose_name='Amount')),
                ('data', jsonfield.fields.JSONField(blank=True, null=True, verbose_name='Serialized extra data')),
            ],
            options={
                'verbose_name': 'Extra order item price field',
                'verbose_name_plural': 'Extra order item price fields',
            },
        ),
        migrations.CreateModel(
            name='ExtraOrderPriceField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('value', drop.util.fields.CurrencyField(decimal_places=2, default=Decimal('0.0'), max_digits=30, verbose_name='Amount')),
                ('data', jsonfield.fields.JSONField(blank=True, null=True, verbose_name='Serialized extra data')),
                ('is_shipping', models.BooleanField(default=False, editable=False, verbose_name='Is shipping')),
            ],
            options={
                'verbose_name': 'Extra order price field',
                'verbose_name_plural': 'Extra order price fields',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(10, 'Processing'), (20, 'Confirming'), (30, 'Confirmed'), (40, 'Paid'), (50, 'Shipped'), (-10, 'Refunded')], default=10, verbose_name='Status')),
                ('order_subtotal', drop.util.fields.CurrencyField(decimal_places=2, default=Decimal('0.0'), max_digits=30, verbose_name='Order subtotal')),
                ('order_total', drop.util.fields.CurrencyField(decimal_places=2, default=Decimal('0.0'), max_digits=30, verbose_name='Order Total')),
                ('shipping_address_text', models.TextField(blank=True, null=True, verbose_name='Shipping address')),
                ('billing_address_text', models.TextField(blank=True, null=True, verbose_name='Billing address')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('cart_pk', models.PositiveIntegerField(blank=True, null=True, verbose_name='Cart primary key')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderExtraInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, verbose_name='Extra info')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_info', to='drop.Order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Order extra info',
                'verbose_name_plural': 'Order extra info',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_reference', models.CharField(max_length=255, verbose_name='Product reference')),
                ('product_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Product name')),
                ('unit_price', drop.util.fields.CurrencyField(decimal_places=2, default=Decimal('0.0'), max_digits=30, verbose_name='Unit price')),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('line_subtotal', drop.util.fields.CurrencyField(decimal_places=2, default=Decimal('0.0'), max_digits=30, verbose_name='Line subtotal')),
                ('line_total', drop.util.fields.CurrencyField(decimal_places=2, default=Decimal('0.0'), max_digits=30, verbose_name='Line total')),
                ('extra', jsonfield.fields.JSONField(default=dict)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='drop.Order', verbose_name='Order')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Order item',
                'verbose_name_plural': 'Order items',
            },
        ),
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', drop.util.fields.CurrencyField(decimal_places=2, default=Decimal('0.0'), max_digits=30, verbose_name='Amount')),
                ('transaction_id', models.CharField(help_text="The transaction processor's reference", max_length=255, verbose_name='Transaction ID')),
                ('backend', models.CharField(help_text='The payment backend used to process the purchase', max_length=255, verbose_name='Payment backend')),
                ('description', models.CharField(max_length=255)),
                ('refunded', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drop.Order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Order payment',
                'verbose_name_plural': 'Order payments',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date added')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
                ('unit_price', drop.util.fields.CurrencyField(decimal_places=2, default=0, max_digits=30, verbose_name='Unit price')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('categories', models.ManyToManyField(blank=True, to='drop.Category')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_drop.product_set+', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-date_added',),
                'abstract': False,
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
            bases=(models.Model, lablackey.unrest.JsonMixin),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='drop.Product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='extraorderpricefield',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drop.Order', verbose_name='Order'),
        ),
        migrations.AddField(
            model_name='extraorderitempricefield',
            name='order_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drop.OrderItem', verbose_name='Order item'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drop.Product'),
        ),
    ]
