# Generated by Django 4.0.5 on 2022-07-10 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_product_p_image1_product_p_image2_product_p_image3_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='month',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='product',
            name='year',
        ),
    ]