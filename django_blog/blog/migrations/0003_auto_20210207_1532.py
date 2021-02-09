# Generated by Django 3.1.6 on 2021-02-07 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210206_0213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='status',
        ),
        migrations.RemoveField(
            model_name='post',
            name='status',
        ),
        migrations.AddField(
            model_name='comment',
            name='is_accepted',
            field=models.BooleanField(default=False, verbose_name='تایید شده'),
        ),
        migrations.AddField(
            model_name='comment',
            name='is_activated',
            field=models.BooleanField(default=False, verbose_name='فعال شده'),
        ),
        migrations.AddField(
            model_name='post',
            name='is_accepted',
            field=models.BooleanField(default=False, verbose_name='تایید شده'),
        ),
        migrations.AddField(
            model_name='post',
            name='is_activated',
            field=models.BooleanField(default=False, verbose_name='فعال شده'),
        ),
    ]