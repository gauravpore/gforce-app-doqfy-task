# Generated by Django 4.2.3 on 2023-07-15 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gforce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=100),
        ),
    ]
