# Generated by Django 3.2.21 on 2023-09-07 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]