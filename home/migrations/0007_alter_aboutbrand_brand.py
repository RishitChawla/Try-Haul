# Generated by Django 5.1.3 on 2025-03-18 08:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_aboutbrand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutbrand',
            name='brand',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.brand'),
        ),
    ]
