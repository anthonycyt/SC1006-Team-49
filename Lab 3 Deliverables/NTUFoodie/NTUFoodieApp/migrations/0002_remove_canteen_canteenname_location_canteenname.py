# Generated by Django 5.1.2 on 2024-10-27 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NTUFoodieApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='canteen',
            name='canteenName',
        ),
        migrations.AddField(
            model_name='location',
            name='canteenName',
            field=models.CharField(max_length=200, null=True),
        ),
    ]