# Generated by Django 4.0.5 on 2022-07-09 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_user_u_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phoneno',
            new_name='phone_no',
        ),
    ]
