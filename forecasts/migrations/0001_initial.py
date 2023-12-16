# Generated by Django 4.2.8 on 2023-12-16 08:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('forecast_no', models.CharField(blank=True, max_length=15, null=True, verbose_name='Request No.')),
                ('forecast_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Request Date')),
                ('forecast_item', models.IntegerField(blank=True, default='0', null=True, verbose_name='Item')),
                ('forecast_qty', models.FloatField(blank=True, default='0', null=True, verbose_name='Qty.')),
                ('forecast_total_qty', models.FloatField(blank=True, default='0', null=True, verbose_name='Total Qty.')),
                ('forecast_price', models.FloatField(blank=True, default='0', null=True, verbose_name='Price.')),
                ('forecast_m0', models.FloatField(blank=True, default='0', null=True, verbose_name='Month 0')),
                ('forecast_m1', models.FloatField(blank=True, default='0', null=True, verbose_name='Month 1')),
                ('forecast_m2', models.FloatField(blank=True, default='0', null=True, verbose_name='Month 2')),
                ('forecast_m3', models.FloatField(blank=True, default='0', null=True, verbose_name='Month 3')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='Remark')),
                ('forecast_status', models.CharField(choices=[('0', 'รออนุมัติ'), ('1', 'อนุมัติแล้ว'), ('2', 'เปิด PR แล้ว'), ('3', 'เปิด PDS แล้ว'), ('4', 'ไม่อนุมัติ'), ('5', 'ยกเลิก')], default='0', max_length=1, verbose_name='Request Status')),
                ('forecast_download_count', models.IntegerField(blank=True, default='0', null=True, verbose_name='Download Count')),
                ('file_estimate_forecast', models.FileField(blank=True, null=True, upload_to='static/estimated_forecasts', verbose_name='Upload Estimated Forecast')),
                ('ref_formula_id', models.CharField(blank=True, max_length=8, null=True, verbose_name='Ref. Formula ID')),
                ('is_po', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is PO')),
                ('is_sync', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is Sync')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Forecast',
                'verbose_name_plural': 'EDI Forecast',
                'db_table': 'ediForecast',
                'ordering': ('forecast_status', 'forecast_date', 'forecast_no'),
                'permissions': [('approve_reject', 'จัดการ Approve/Reject'), ('is_download_report', 'ดูรายงาน'), ('upload_file_estimated_forecast', 'อัพโหลด ESF'), ('upload_file_forecast', 'อัพโหลด Forecast')],
                'default_permissions': ['view'],
            },
        ),
        migrations.CreateModel(
            name='ForecastDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('seq', models.IntegerField(blank=True, default='0', null=True, verbose_name='#')),
                ('request_qty', models.IntegerField(default='0.0', verbose_name='Request Qty.')),
                ('balance_qty', models.IntegerField(default='0.0', verbose_name='Total Qty.')),
                ('price', models.FloatField(blank=True, default='0', null=True, verbose_name='Price.')),
                ('month_0', models.IntegerField(blank=True, default='0', null=True, verbose_name='Month 0')),
                ('month_1', models.IntegerField(blank=True, default='0', null=True, verbose_name='Month 1')),
                ('month_2', models.IntegerField(blank=True, default='0', null=True, verbose_name='Month 2')),
                ('month_3', models.IntegerField(blank=True, default='0', null=True, verbose_name='Month 3')),
                ('request_status', models.CharField(choices=[('0', 'รออนุมัติ'), ('1', 'อนุมัติแล้ว'), ('2', 'เปิด PR แล้ว'), ('3', 'เปิด PDS แล้ว'), ('4', 'ไม่อนุมัติ'), ('5', 'ยกเลิก')], default='0', max_length=1, verbose_name='Request Status')),
                ('import_model_by_user', models.CharField(blank=True, max_length=255, null=True, verbose_name='Model')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='Remark')),
                ('is_selected', models.BooleanField(default=False, verbose_name='Is Selected')),
                ('is_sync', models.BooleanField(default=True, verbose_name='Is Sync')),
                ('ref_formula_id', models.CharField(blank=True, max_length=8, null=True, verbose_name='Ref. Formula ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('forecast_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forecasts.forecast', verbose_name='Open PDS ID')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Product Code')),
            ],
            options={
                'verbose_name': 'ForecastDetail',
                'verbose_name_plural': 'Forecast Detail',
                'db_table': 'ediForecastDetail',
                'ordering': ('seq', 'product_id', 'created_at', 'updated_at'),
                'permissions': [('edit_qty_price', 'แก้ไขจำนวนและราคา'), ('select_item', 'เลือกรายการสินค้า')],
            },
        ),
    ]
