# Generated by Django 4.2.8 on 2023-12-21 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
        ('products', '0001_initial'),
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forecasts', '0001_initial'),
        ('upload_forecasts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckLastPurchaseRunning',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('last_date', models.CharField(max_length=4)),
                ('last_running', models.CharField(max_length=8, unique=True)),
                ('last_no', models.CharField(max_length=15, unique=True)),
                ('is_active', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Active')),
            ],
            options={
                'db_table': 'tempLastPurchaseRunning',
            },
        ),
        migrations.CreateModel(
            name='ReportPDSHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factory_tags', models.CharField(max_length=50, verbose_name='Factory Tags')),
                ('delivery_date', models.CharField(max_length=50, verbose_name='Delivery Date')),
                ('sup_code', models.CharField(max_length=50, verbose_name='Sup. Code')),
                ('sup_name', models.CharField(max_length=255, verbose_name='Sup. Name')),
                ('sup_telephone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Sup. Telephone')),
                ('pds_no', models.CharField(max_length=50, unique=True, verbose_name='PDS No.')),
                ('issue_date', models.CharField(max_length=50, verbose_name='Issue Date')),
                ('issue_time', models.CharField(blank=True, max_length=50, null=True, verbose_name='Issue Time')),
                ('approve_by_id', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Approve By ID')),
                ('issue_by_id', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Issue By ID')),
                ('issue_by_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Issue By Name')),
                ('is_active', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tempReportPDSHeader',
            },
        ),
        migrations.CreateModel(
            name='ReportPDSDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seq', models.IntegerField(verbose_name='Seq.')),
                ('part_model', models.CharField(blank=True, max_length=50, null=True, verbose_name='Part Model')),
                ('part_code', models.CharField(max_length=50, verbose_name='Part Code')),
                ('part_name', models.CharField(max_length=255, verbose_name='Part Name')),
                ('packing_qty', models.IntegerField(verbose_name='Packing')),
                ('total', models.IntegerField(verbose_name='Total')),
                ('is_active', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pds_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='open_pds.reportpdsheader', verbose_name='PDS Header')),
            ],
            options={
                'db_table': 'tempReportPDSDetail',
            },
        ),
        migrations.CreateModel(
            name='PDSHeader',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('pds_date', models.DateField(blank=True, null=True, verbose_name='PDS Date')),
                ('pds_delivery_date', models.DateField(blank=True, null=True, verbose_name='Delivery Date')),
                ('pds_no', models.CharField(blank=True, max_length=15, null=True, verbose_name='PDS No.')),
                ('item', models.IntegerField(verbose_name='Item')),
                ('qty', models.IntegerField(verbose_name='Qty')),
                ('balance_qty', models.IntegerField(blank=True, default='0', null=True, verbose_name='Total Qty')),
                ('summary_price', models.FloatField(blank=True, default='0', null=True, verbose_name='Summary Price')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='Remark')),
                ('pds_status', models.CharField(blank=True, choices=[(0, 'รอเปิด PDS'), (1, 'เปิด PDS บางส่วน'), (2, 'เสร็จสมบูรณ์'), (3, 'ยกเลิก'), (4, 'ถูกยกเลิก PDS')], default='0', max_length=1, null=True, verbose_name='PDS Status')),
                ('pds_download_count', models.IntegerField(blank=True, null=True, verbose_name='Download Count')),
                ('ref_formula_id', models.CharField(blank=True, max_length=8, null=True, verbose_name='Formula ID')),
                ('is_active', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approve_by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Approve By ID')),
                ('forecast_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='forecasts.forecast', verbose_name='PR No.')),
                ('forecast_plan_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.planningforecast', verbose_name='Forecast Plan')),
                ('part_model_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.productgroup', verbose_name='Model ID')),
                ('pds_on_month_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='upload_forecasts.onmonthlist', verbose_name='Request On Month')),
                ('pds_on_year_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='upload_forecasts.onyearlist', verbose_name='Request On Year')),
                ('pds_revise_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='books.edirevisetype', verbose_name='Revise ID')),
                ('supplier_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.supplier', verbose_name='Supplier ID')),
            ],
            options={
                'verbose_name': 'PDS',
                'verbose_name_plural': 'Open PDS',
                'db_table': 'ediPDS',
                'ordering': ('pds_status', 'pds_no', 'created_at', 'updated_at'),
                'permissions': [('create_purchase_order', 'เปิด PO'), ('is_download_report', 'ดูรายงาน'), ('add_new_item', 'เพิ่มรายการใหม่'), ('edit_qty', 'แก้ไขจำนวน'), ('edit_price', 'แก้ไขราคา'), ('print_tag', 'Print TAG')],
            },
        ),
        migrations.CreateModel(
            name='PDSDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('seq', models.IntegerField(verbose_name='Seq.')),
                ('qty', models.IntegerField(verbose_name='Qty')),
                ('balance_qty', models.IntegerField(blank=True, default='0', null=True, verbose_name='Total Qty')),
                ('price', models.FloatField(blank=True, default='0', null=True, verbose_name='Price')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='Remark')),
                ('ref_formula_id', models.CharField(blank=True, max_length=8, null=True, verbose_name='Formula ID')),
                ('pds_detail_status', models.CharField(blank=True, choices=[(0, 'รอเปิด PDS'), (1, 'เปิด PDS บางส่วน'), (2, 'เสร็จสมบูรณ์'), (3, 'ยกเลิก'), (4, 'ถูกยกเลิก PDS')], default='0', max_length=1, null=True, verbose_name='PDS Status')),
                ('is_select', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is Select')),
                ('is_active', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('forecast_detail_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forecasts.forecastdetail', verbose_name='PDS Detail')),
                ('pds_header_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='open_pds.pdsheader', verbose_name='PDS ID')),
            ],
            options={
                'verbose_name': 'PDSDetail',
                'verbose_name_plural': 'PDS Detail',
                'db_table': 'ediPDSDetail',
                'ordering': ('seq', 'forecast_detail_id', 'created_at', 'updated_at'),
            },
        ),
    ]
