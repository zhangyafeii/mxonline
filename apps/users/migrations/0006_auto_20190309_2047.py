# Generated by Django 2.1.7 on 2019-03-09 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190309_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '找回密码'), ('update_email', '修改邮箱')], max_length=10, verbose_name='验证码类型'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(default='', max_length=100, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='female', max_length=6, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='image/default.png', null=True, upload_to='image/%Y/%m', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号'),
        ),
    ]