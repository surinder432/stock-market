# Generated by Django 3.0.1 on 2020-07-10 13:58

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DematTxn',
            fields=[
                ('stock_symbol', models.TextField(blank=True, null=True)),
                ('company_name', models.TextField(primary_key=True, serialize=False)),
                ('isin_code', models.TextField(blank=True, null=True)),
                ('action', models.TextField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('txn_price', models.FloatField(blank=True, null=True)),
                ('brokerage', models.TextField(blank=True, null=True)),
                ('txn_charges', models.TextField(blank=True, null=True)),
                ('stamp_duty', models.TextField(blank=True, null=True)),
                ('segment', models.TextField(blank=True, null=True)),
                ('stt', models.TextField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('txn_date', models.DateField(blank=True, null=True)),
                ('exchange', models.TextField(blank=True, null=True)),
                ('unused1', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_demat_txn',
                'unique_together': {('company_name', 'txn_date')},
            },
        ),
    ]
