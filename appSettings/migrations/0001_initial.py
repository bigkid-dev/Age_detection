# Generated by Django 4.1.6 on 2023-11-05 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='settings_name', max_length=256)),
                ('value', models.CharField(blank=True, default='', max_length=256)),
            ],
        ),
    ]
