# Generated by Django 2.1.7 on 2019-03-04 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20190304_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='course_nums',
            field=models.IntegerField(default=0, verbose_name='课程数'),
        ),
    ]