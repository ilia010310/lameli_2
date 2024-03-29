# Generated by Django 5.0.1 on 2024-02-01 18:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='avatar',
            field=models.ImageField(default='default.png', upload_to='images/avatars/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif', 'webp'))], verbose_name='Главная фотография'),
        ),
    ]
