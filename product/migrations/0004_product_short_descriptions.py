# Generated by Django 5.0.6 on 2024-06-11 05:28

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_product_game_remove_product_icon_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_descriptions',
            field=ckeditor.fields.RichTextField(default=1, verbose_name='Enter Short Descriptions'),
            preserve_default=False,
        ),
    ]
