# Generated by Django 5.2.1 on 2025-05-14 09:59

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('debts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Payment Amount')),
                ('debt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='debts.debt', verbose_name='Debt')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
