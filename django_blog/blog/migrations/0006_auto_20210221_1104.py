# Generated by Django 3.1.6 on 2021-02-21 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210219_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentlike',
            name='value',
            field=models.BooleanField(choices=[(True, 'like'), (False, 'dislike')], default=True, verbose_name='مقدار'),
        ),
        migrations.AlterField(
            model_name='postlike',
            name='value',
            field=models.BooleanField(choices=[(True, 'like'), (False, 'dislike')], default=True, verbose_name='مقدار'),
        ),
    ]
