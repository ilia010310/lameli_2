# Generated by Django 5.0.1 on 2024-01-30 21:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='product',
            name='avatar',
            field=models.ImageField(blank=True, default='default.png', upload_to='images/avatars/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))], verbose_name='Главная фотография'),
        ),
    ]
