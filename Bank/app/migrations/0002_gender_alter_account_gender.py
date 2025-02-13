# Generated by Django 5.1.5 on 2025-02-05 08:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=7)),
            ],
        ),
        migrations.AlterField(
            model_name='account',
            name='gender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.gender'),
        ),
    ]
