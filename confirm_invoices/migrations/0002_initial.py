# Generated by Django 4.2.8 on 2023-12-16 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('open_pds', '0001_initial'),
        ('confirm_invoices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirminvoiceheader',
            name='approve_by_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Approve By ID'),
        ),
        migrations.AddField(
            model_name='confirminvoiceheader',
            name='part_model_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.productgroup', verbose_name='Model ID'),
        ),
        migrations.AddField(
            model_name='confirminvoiceheader',
            name='pds_id',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='open_pds.pdsheader', verbose_name='PR No.'),
        ),
        migrations.AddField(
            model_name='confirminvoiceheader',
            name='supplier_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.supplier', verbose_name='Supplier ID'),
        ),
        migrations.AddField(
            model_name='confirminvoicedetail',
            name='invoice_header_id',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='confirm_invoices.confirminvoiceheader', verbose_name='PDS ID'),
        ),
        migrations.AddField(
            model_name='confirminvoicedetail',
            name='pds_detail_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='open_pds.pdsdetail', verbose_name='PDS Detail'),
        ),
    ]
