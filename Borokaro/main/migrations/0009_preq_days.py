# Generated by Django 4.0.5 on 2022-07-10 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_preq'),
    ]

    operations = [
        migrations.AddField(
            model_name='preq',
            name='days',
            field=models.IntegerField(default=5),
        ),
    ]
