# Generated by Django 5.1.3 on 2025-03-22 20:11

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('IsFeatured', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('hexCode', models.CharField(help_text='Hex code for color', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_label', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('firstName', models.CharField(max_length=30)),
                ('lastName', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('uniqueLabel', models.PositiveIntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discountedPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('productDetails', models.TextField(blank=True, null=True)),
                ('deliveryTime', models.CharField(default='5-7 days', max_length=255)),
                ('stockQuantity', models.PositiveIntegerField(default=0)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('returnEligible', models.BooleanField(default=False)),
                ('exchangeEligible', models.BooleanField(default=False)),
                ('bestSelling', models.BooleanField(default=False)),
                ('newArrival', models.BooleanField(default=False)),
                ('specialOffer', models.BooleanField(default=False)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.category')),
                ('colors', models.ManyToManyField(to='home.color')),
                ('productType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.producttype')),
                ('sizes', models.ManyToManyField(to='home.size')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='home.listing')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cartQuantity', models.IntegerField(default=1)),
                ('cartUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartUser', to=settings.AUTH_USER_MODEL)),
                ('cartItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartItem', to='home.listing')),
                ('cartSize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='size', to='home.size')),
            ],
        ),
        migrations.CreateModel(
            name='SizeGuide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chest', models.FloatField()),
                ('waist', models.FloatField()),
                ('hip', models.FloatField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.brand')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.size')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wishlistItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlistedItem', to='home.listing')),
                ('wishlistUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlistUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='listing',
            constraint=models.UniqueConstraint(fields=('productType', 'uniqueLabel'), name='unique_product_label'),
        ),
    ]
