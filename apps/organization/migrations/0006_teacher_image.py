# Generated by Django 2.1.7 on 2019-03-04 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20190304_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='teacher/%Y/%m', verbose_name='头像'),
        ),
    ]
