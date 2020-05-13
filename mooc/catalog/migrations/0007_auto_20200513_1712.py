# Generated by Django 3.0.5 on 2020-05-13 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0006_auto_20200504_1614'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mycourse',
            options={'ordering': ['last_accessed']},
        ),
        migrations.AlterField(
            model_name='mycourse',
            name='active',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
