# Generated by Django 4.1.2 on 2022-11-21 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('bday', models.DateField()),
            ],
            options={
                'db_table': 'Userinfo',
            },
        ),
    ]
