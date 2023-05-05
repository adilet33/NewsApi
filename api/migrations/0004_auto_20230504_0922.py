# Generated by Django 3.2.12 on 2023-05-04 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20230504_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('author', 'Author'), ('user', 'User')], default='user', max_length=6, verbose_name='choice role'),
        ),
        migrations.CreateModel(
            name='UserNewsPostRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='likes')),
                ('save', models.BooleanField(default=False, verbose_name='save')),
                ('newsPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.newspost', verbose_name='news')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]