# Generated by Django 2.1.3 on 2018-11-05 21:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='127.0.0.1', max_length=255, verbose_name='DNS/IP Server')),
                ('port', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(65535)], verbose_name='Port')),
                ('server_type', models.CharField(choices=[('bind9', 'Bind 9 DNS server')], default='bind9', editable=False, max_length=8, verbose_name='Type server')),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('zone_id', models.AutoField(primary_key=True, serialize=False)),
                ('path_file', models.CharField(max_length=4096, verbose_name='Zone file path')),
                ('zone_name', models.CharField(default='None', max_length=255, unique=True)),
                ('zone_type', models.CharField(choices=[('forward', 'forward zone'), ('reverse', 'reverse zone')], default='forward', max_length=8, verbose_name='Type zone')),
                ('zone_text', models.TextField(blank=True, verbose_name='Text zone view')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='editor.Service', verbose_name='Server')),
            ],
        ),
    ]
