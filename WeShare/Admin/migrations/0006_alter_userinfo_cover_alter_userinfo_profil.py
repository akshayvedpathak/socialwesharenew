# Generated by Django 4.1.2 on 2022-11-27 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0005_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='cover',
            field=models.ImageField(default='pqr.jpg', upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='profil',
            field=models.ImageField(default='abc.jpg', upload_to='Images/'),
        ),
    ]
