# Generated by Django 3.1 on 2020-10-04 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_auto_20201004_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbadge',
            name='badg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.badges'),
        ),
    ]