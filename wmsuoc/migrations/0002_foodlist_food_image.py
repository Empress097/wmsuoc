# Generated by Django 4.2.5 on 2023-10-17 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wmsuoc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodlist',
            name='food_image',
            field=models.ImageField(blank=True, null=True, upload_to='food', verbose_name='Food Image'),
        ),
    ]
