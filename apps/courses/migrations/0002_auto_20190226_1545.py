# Generated by Django 2.1.7 on 2019-02-26 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='degree',
            field=models.IntegerField(choices=[(0, '初级'), (1, '中级'), (2, '高级')], verbose_name='课程难度'),
        ),
    ]
