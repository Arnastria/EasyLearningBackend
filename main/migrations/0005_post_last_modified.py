# Generated by Django 3.1.2 on 2021-02-18 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210217_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]