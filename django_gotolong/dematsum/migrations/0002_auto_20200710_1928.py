# Generated by Django 3.0.1 on 2020-07-10 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('amfi', '0002_auto_20200710_1928'),
        ('dematsum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DematSum',
            fields=[
                ('stock_symbol', models.TextField(blank=True, null=True)),
                ('company_name', models.TextField(primary_key=True, serialize=False)),
                ('qty', models.TextField(blank=True, null=True)),
                ('acp', models.TextField(blank=True, null=True)),
                ('cmp', models.TextField(blank=True, null=True)),
                ('pct_change', models.TextField(blank=True, null=True)),
                ('value_cost', models.TextField(blank=True, null=True)),
                ('value_market', models.TextField(blank=True, null=True)),
                ('days_gain', models.TextField(blank=True, null=True)),
                ('days_gain_pct', models.TextField(blank=True, null=True)),
                ('realized_pl', models.TextField(blank=True, null=True)),
                ('unrealized_pl', models.TextField(blank=True, null=True)),
                ('unrealized_pl_pct', models.TextField(blank=True, null=True)),
                ('unused1', models.TextField(blank=True, null=True)),
                ('isin_code', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='amfi.Amfi')),
            ],
            options={
                'db_table': 'user_demat_sum',
            },
        ),
        migrations.DeleteModel(
            name='DematSummary',
        ),
    ]
