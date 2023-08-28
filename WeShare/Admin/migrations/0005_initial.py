# Generated by Django 4.1.2 on 2022-11-24 15:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Admin', '0004_delete_userinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
                ('phone', models.IntegerField()),
                ('profil', models.ImageField(default='abc.jpg', upload_to='Images')),
                ('cover', models.ImageField(default='pqr.jpg', upload_to='Images')),
                ('Bio', models.CharField(max_length=500)),
                ('location', models.CharField(max_length=20)),
                ('bday', models.DateTimeField(default=datetime.datetime.now)),
                ('joining', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'Userinfo',
            },
        ),
    ]
