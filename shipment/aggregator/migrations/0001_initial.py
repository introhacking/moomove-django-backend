# Generated by Django 5.0.6 on 2024-10-25 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comodity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_uuid', models.CharField(editable=False, max_length=16, null=True, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('soft_delete', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_uuid', models.CharField(editable=False, max_length=16, null=True, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('soft_delete', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FreightType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('soft_delete', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IncoTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_uuid', models.CharField(editable=False, max_length=16, null=True, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('soft_delete', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransitTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=60)),
                ('cust_name', models.CharField(max_length=100)),
                ('cust_email', models.EmailField(max_length=80)),
                ('sales_represent', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=20)),
                ('terms_condition', models.CharField(default='Terms & Condition', max_length=256)),
            ],
            options={
                'unique_together': {('cust_name', 'cust_email', 'sales_represent', 'phone', 'terms_condition')},
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=70)),
            ],
            options={
                'unique_together': {('name', 'email', 'username', 'password', 'phone')},
            },
        ),
        migrations.CreateModel(
            name='VersionedRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_uuid', models.CharField(editable=False, max_length=16, null=True, unique=True)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='USD', max_length=15)),
                ('free_days', models.IntegerField(default='1')),
                ('free_days_comment', models.CharField(default='testing', max_length=256, null=True)),
                ('spot_filed', models.CharField(default='spot', max_length=15)),
                ('isRateTypeStatus', models.BooleanField(blank=True, default=False, null=True)),
                ('isRateUsed', models.BooleanField(default=False)),
                ('transhipment_add_port', models.CharField(blank=True, max_length=50, null=True)),
                ('effective_date', models.DateField()),
                ('cargotype', models.CharField(max_length=50, null=True)),
                ('vessel_name', models.CharField(max_length=50, null=True)),
                ('voyage', models.CharField(max_length=50, null=True)),
                ('haz_class', models.CharField(max_length=50, null=True)),
                ('packing_group', models.CharField(max_length=50, null=True)),
                ('hazardous', models.BooleanField(default=False, null=True)),
                ('un_number', models.CharField(max_length=4, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('terms_condition', models.CharField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_current', models.BooleanField(default=True)),
                ('soft_delete', models.BooleanField(blank=True, default=False, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.company')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.destination')),
                ('freight_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.freighttype')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.source')),
                ('transit_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.transittime')),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_uuid', models.CharField(editable=False, max_length=16, null=True, unique=True)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='USD', max_length=15)),
                ('free_days', models.IntegerField(default='1')),
                ('free_days_comment', models.CharField(default='testing', max_length=256, null=True)),
                ('spot_filed', models.CharField(default='spot', max_length=15)),
                ('isRateTypeStatus', models.BooleanField(blank=True, default=False, null=True)),
                ('isRateUsed', models.BooleanField(default=False)),
                ('transhipment_add_port', models.CharField(blank=True, max_length=50, null=True)),
                ('effective_date', models.DateField()),
                ('cargotype', models.CharField(max_length=50, null=True)),
                ('vessel_name', models.CharField(max_length=50, null=True)),
                ('voyage', models.CharField(max_length=50, null=True)),
                ('haz_class', models.CharField(max_length=50, null=True)),
                ('packing_group', models.CharField(max_length=50, null=True)),
                ('hazardous', models.BooleanField(default=False, null=True)),
                ('un_number', models.CharField(max_length=4, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('terms_condition', models.CharField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('soft_delete', models.BooleanField(blank=True, default=False, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.company')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.destination')),
                ('freight_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.freighttype')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.source')),
                ('transit_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.transittime')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='aggregator.versionedrate')),
            ],
            options={
                'unique_together': {('company', 'source', 'destination', 'transit_time', 'freight_type', 'currency', 'spot_filed', 'vessel_name', 'voyage', 'haz_class', 'packing_group', 'terms_condition', 'free_days', 'free_days_comment', 'hazardous', 'un_number', 'effective_date', 'expiration_date', 'soft_delete')},
            },
        ),
        migrations.CreateModel(
            name='ManualRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_uuid', models.CharField(editable=False, max_length=16, unique=True)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('free_days', models.IntegerField(default='1')),
                ('free_days_comment', models.CharField(default='testing', max_length=256, null=True)),
                ('currency', models.CharField(default='USD', max_length=15)),
                ('effective_date', models.DateField()),
                ('cargotype', models.CharField(max_length=50, null=True)),
                ('vessel_name', models.CharField(max_length=50, null=True)),
                ('voyage', models.CharField(max_length=50, null=True)),
                ('haz_class', models.CharField(max_length=50, null=True)),
                ('packing_group', models.CharField(max_length=50, null=True)),
                ('hazardous', models.BooleanField(default=False, null=True)),
                ('un_number', models.CharField(max_length=4, null=True)),
                ('direct_shipment', models.BooleanField(blank=True, default=False, null=True)),
                ('spot_filed', models.CharField(default='spot', max_length=15)),
                ('isRateTypeStatus', models.BooleanField(blank=True, default=False, null=True)),
                ('isRateUsed', models.BooleanField(default=False)),
                ('transhipment_add_port', models.CharField(blank=True, max_length=50, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('terms_condition', models.CharField(blank=True, null=True)),
                ('soft_delete', models.BooleanField(blank=True, default=False, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='aggregator.company')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.destination')),
                ('freight_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.freighttype')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.source')),
                ('transit_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.transittime')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manualrates', to='aggregator.versionedrate')),
            ],
            options={
                'unique_together': {('company', 'destination', 'source', 'direct_shipment', 'spot_filed', 'vessel_name', 'voyage', 'haz_class', 'packing_group', 'free_days', 'free_days_comment', 'hazardous', 'un_number', 'transhipment_add_port', 'cargotype', 'transit_time', 'freight_type', 'rate', 'currency', 'effective_date', 'expiration_date', 'remarks', 'terms_condition', 'soft_delete', 'version')},
            },
        ),
    ]
