# Generated by Django 2.1.7 on 2019-03-09 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_auto_20190306_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(default='全国知名', max_length=10, verbose_name='机构标签'),
        ),
    ]
