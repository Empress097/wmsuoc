# Generated by Django 4.2.5 on 2023-10-17 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wmsuoc', '0002_foodlist_food_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Food Title')),
                ('slug', models.SlugField(max_length=160, verbose_name='Food Slug')),
                ('sku', models.CharField(max_length=255, unique=True, verbose_name='Unique Food ID (SKU)')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_active', models.BooleanField(verbose_name='Is Active?')),
                ('food_image', models.ImageField(blank=True, null=True, upload_to='food', verbose_name='Food Image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wmsuoc.category', verbose_name='Product Category')),
            ],
        ),
        migrations.DeleteModel(
            name='FoodList',
        ),
        migrations.AddField(
            model_name='cart',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wmsuoc.product', verbose_name='Foodlist'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]