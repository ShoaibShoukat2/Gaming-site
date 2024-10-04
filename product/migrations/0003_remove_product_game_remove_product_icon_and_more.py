# Generated by Django 5.0.6 on 2024-06-11 05:15

import autoslug.fields
import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='game',
        ),
        migrations.RemoveField(
            model_name='product',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='games_category', to='product.category', verbose_name='Select Product Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='descriptions',
            field=ckeditor.fields.RichTextField(default=1, verbose_name='Descriptions'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(default=1, upload_to='ProductImage/', verbose_name='Select Product Image'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='product_name', unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='name', unique=True),
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=150, verbose_name='Enter Product Item Name')),
                ('item_icon', models.ImageField(upload_to='ProductImage/', verbose_name='Select Product Item Icon')),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Enter Product Item Price')),
                ('slug', autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='item_name', unique=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.product', verbose_name='Select Product')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.DeleteModel(
            name='Game',
        ),
    ]