# Generated by Django 4.0.5 on 2022-07-09 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_user_address_alter_user_u_type_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='u_id',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='product',
            name='p_image1',
        ),
        migrations.RemoveField(
            model_name='product',
            name='p_image2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='p_image3',
        ),
        migrations.CreateModel(
            name='ProdImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prodimage', to='main.product')),
            ],
        ),
    ]
