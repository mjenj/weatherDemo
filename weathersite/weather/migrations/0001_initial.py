# Generated by Django 2.2.28 on 2023-02-21 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_text', models.CharField(max_length=200)),
                ('request_date', models.DateTimeField(verbose_name='date requested')),
            ],
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_response', models.CharField(max_length=400)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.Request')),
            ],
        ),
    ]
