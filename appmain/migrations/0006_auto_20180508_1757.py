# Generated by Django 2.0.3 on 2018-05-08 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appmain', '0005_auto_20180506_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixationaccident',
            name='accident_type',
            field=models.ManyToManyField(to='appmain.Accident'),
        ),
    ]
