# Generated by Django 3.2.12 on 2023-05-04 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20230504_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernewspostrelation',
            name='like',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usernewspostrelation',
            name='save',
            field=models.BooleanField(default=False),
        ),
    ]
