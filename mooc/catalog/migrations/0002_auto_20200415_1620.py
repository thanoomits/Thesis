# Generated by Django 3.0.5 on 2020-04-15 13:20

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Courses',
            new_name='Course',
        ),
        migrations.RenameModel(
            old_name='Postedby',
            new_name='Teacher',
        ),
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
    ]
