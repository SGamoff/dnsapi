# Generated by Django 2.1.3 on 2018-11-12 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='server_type',
            field=models.CharField(choices=[('BIND9', 'bind9')], default='bind9', editable=False, max_length=8, verbose_name='Type server'),
        ),
        migrations.AlterField(
            model_name='zone',
            name='zone_type',
            field=models.CharField(choices=[('FWD', 'forward'), ('RVS', 'reverse')], default='forward', max_length=8, verbose_name='Type zone'),
        ),
    ]