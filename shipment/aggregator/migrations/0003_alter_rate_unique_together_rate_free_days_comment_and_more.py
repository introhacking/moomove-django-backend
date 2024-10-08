# Generated by Django 5.0.6 on 2024-10-10 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0002_alter_manualrate_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rate',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='rate',
            name='free_days_comment',
            field=models.CharField(default='testing', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='hazardous',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='un_number',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='versionedrate',
            name='free_days_comment',
            field=models.CharField(default='testing', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='versionedrate',
            name='hazardous',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='versionedrate',
            name='un_number',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='rate',
            unique_together={('company', 'source', 'destination', 'transit_time', 'freight_type', 'spot_filed', 'free_days', 'free_days_comment', 'hazardous', 'un_number', 'effective_date', 'expiration_date', 'soft_delete')},
        ),
    ]
