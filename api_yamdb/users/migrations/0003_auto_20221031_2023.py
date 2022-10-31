# Generated by Django 2.2.16 on 2022-10-31 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin'), ('superuser', 'superuser')], default='user', max_length=2),
        ),
    ]
