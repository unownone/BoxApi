# Generated by Django 4.0.1 on 2022-01-15 08:18

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('Inventory', '0002_boxes_date_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constraints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('A1', models.IntegerField(default=100)),
                ('V1', models.IntegerField(default=1000)),
                ('L1', models.IntegerField(default=100)),
                ('L2', models.IntegerField(default=50)),
                ('date_field', models.DateTimeField(default=datetime.datetime(2022, 1, 15, 8, 18, 47, 257804, tzinfo=utc))),
                ('Site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sites.site')),
            ],
        ),
    ]
