# Generated by Django 2.2.16 on 2022-10-31 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('US', 'user'), ('MD', 'moderator'), ('AD', 'admin'), ('SP', 'superuser')], default='user', max_length=2),
        ),
    ]
