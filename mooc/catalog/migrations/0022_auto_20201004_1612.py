# Generated by Django 3.1 on 2020-10-04 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_auto_20201004_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbadge',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.user'),
        ),
    ]
