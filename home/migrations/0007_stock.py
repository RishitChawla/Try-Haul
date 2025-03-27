# Generated by Django 5.1.3 on 2025-03-23 11:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='home.listing')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.size')),
            ],
            options={
                'unique_together': {('listing', 'size')},
            },
        ),
    ]
