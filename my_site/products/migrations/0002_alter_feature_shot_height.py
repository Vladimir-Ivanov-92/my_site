# Generated by Django 4.1.4 on 2023-01-23 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='shot_height',
            field=models.DecimalField(decimal_places=0, max_digits=5, null=True, verbose_name='Высота выстрела (м)'),
        ),
    ]
