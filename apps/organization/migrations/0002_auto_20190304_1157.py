# Generated by Django 2.1.7 on 2019-03-04 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseorg',
            old_name='click_num',
            new_name='click_nums',
        ),
    ]
