# Generated by Django 4.2.8 on 2023-12-19 01:49

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagementUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('avatar_url', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Avatar Image')),
                ('signature_img', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Signature Image')),
                ('is_approve', models.BooleanField(default=False, verbose_name='Is Approve')),
                ('is_issue', models.BooleanField(default=False, verbose_name='Is Issue')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'User',
                'db_table': 'ediUser',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Corporation',
                'verbose_name_plural': 'Corporation',
                'db_table': 'tbmCorporation',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Department',
                'db_table': 'tbmDepartment',
            },
        ),
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Factory',
                'verbose_name_plural': 'Factory',
                'db_table': 'tbmFactory',
            },
        ),
        migrations.CreateModel(
            name='JasperReportServer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('server_name', models.CharField(max_length=255, verbose_name='Server Name')),
                ('server_url', models.CharField(max_length=255, verbose_name='Server URL')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Server Report PDS',
                'verbose_name_plural': 'Server Report PDS',
                'db_table': 'tbmServerReport',
            },
        ),
        migrations.CreateModel(
            name='LineNotification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('token', models.CharField(max_length=50, unique=True, verbose_name='Token Key')),
                ('name', models.CharField(max_length=255, verbose_name='Group Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Line Notification',
                'verbose_name_plural': 'Line Notification',
                'db_table': 'tbmLineNotification',
            },
        ),
        migrations.CreateModel(
            name='PlanningForecast',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('plan_day', models.IntegerField(blank=True, default='1', null=True, verbose_name='Day')),
                ('plan_month', models.CharField(blank=True, choices=[('0', '-'), ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], max_length=2, null=True, verbose_name='On Month')),
                ('plan_year', models.IntegerField(blank=True, null=True, verbose_name='On Year')),
                ('plan_qty', models.IntegerField(blank=True, default='0', null=True, verbose_name='Planning Qty')),
                ('revise_plan_qty', models.IntegerField(blank=True, default='0', null=True, verbose_name='Revise Qty')),
                ('is_active', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'PlanningForecast',
                'verbose_name_plural': 'Planning Forecast',
                'db_table': 'tbmPlanningForecast',
                'ordering': ('plan_year', 'plan_month'),
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Position',
                'verbose_name_plural': 'Position',
                'db_table': 'tbmPosition',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Section',
                'db_table': 'tbmSection',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('code', models.CharField(max_length=150, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Supplier',
                'db_table': 'tbmSupplier',
            },
        ),
        migrations.CreateModel(
            name='UserErrorLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('remark', models.TextField(verbose_name='หมายเหตุ')),
                ('is_status', models.BooleanField(default=False, verbose_name='Success')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User ID')),
            ],
            options={
                'verbose_name': 'Logging Report Handle',
                'verbose_name_plural': 'Logging Report Handle',
                'db_table': 'tbmLoggingReport',
                'ordering': ('-updated_on',),
            },
        ),
        migrations.CreateModel(
            name='ReportIssueByUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('is_active', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User ID')),
            ],
            options={
                'verbose_name': 'Report Issue ByUser',
                'verbose_name_plural': 'Report Issue By User',
                'db_table': 'tbmReportIssueByUser',
            },
        ),
        migrations.CreateModel(
            name='ReportApproveByUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('is_active', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User ID')),
            ],
            options={
                'verbose_name': 'ReportApproveByUser',
                'verbose_name_plural': 'Report Approve By User',
                'db_table': 'tbmReportApproveByUser',
            },
        ),
        migrations.CreateModel(
            name='OrganizationApprovePDS',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('is_active', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approve_by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.reportapprovebyuser', verbose_name='Approve By ID')),
                ('issue_by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.reportissuebyuser', verbose_name='Issue By ID')),
            ],
            options={
                'verbose_name': 'Organize Approve PDS',
                'verbose_name_plural': 'Organize Approve PDS',
                'db_table': 'tbmOrganizationApprovePDS',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('corporation_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.corporation')),
            ],
            options={
                'verbose_name': 'Formula Employee',
                'verbose_name_plural': 'Formula Employee',
                'db_table': 'tbmFormulaEmployee',
            },
        ),
        migrations.AddField(
            model_name='managementuser',
            name='department_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.department', verbose_name='Department ID'),
        ),
        migrations.AddField(
            model_name='managementuser',
            name='factory_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.factory', verbose_name='Factory ID'),
        ),
        migrations.AddField(
            model_name='managementuser',
            name='formula_user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.employee', verbose_name='Formula User ID'),
        ),
        migrations.AddField(
            model_name='managementuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='managementuser',
            name='line_notification_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.linenotification', verbose_name='Line Notification ID'),
        ),
        migrations.AddField(
            model_name='managementuser',
            name='position_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.position', verbose_name='Position ID'),
        ),
        migrations.AddField(
            model_name='managementuser',
            name='section_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.section', verbose_name='Section ID'),
        ),
        migrations.AddField(
            model_name='managementuser',
            name='supplier_id',
            field=models.ManyToManyField(blank=True, related_name='SetSupplier', to='members.supplier', verbose_name='Supplier ID'),
        ),
        migrations.AddField(
            model_name='managementuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
