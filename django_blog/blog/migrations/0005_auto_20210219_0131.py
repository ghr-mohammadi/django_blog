# Generated by Django 3.1.6 on 2021-02-18 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20210218_1138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bloguser',
            options={'ordering': ['-date_joined'], 'verbose_name': 'وبلاگ نویس', 'verbose_name_plural': 'وبلاگ نویسان'},
        ),
    ]
