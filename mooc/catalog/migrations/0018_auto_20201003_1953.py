# Generated by Django 3.1 on 2020-10-03 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_auto_20201003_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rank_status',
            field=models.IntegerField(choices=[('1', 'Bronze'), ('2', 'Silver'), ('3', 'Gold'), ('4', 'Platinum'), ('5', 'Diamond'), ('6', 'Master'), ('7', 'GrandMaster')], default='1', help_text='User Rank'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.IntegerField(choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3'), (4, 'Level 4'), (5, 'Level 5'), (6, 'Level 6'), (7, 'Level 7'), (8, 'Level 8'), (9, 'Level 9'), (10, 'Level 10'), (11, 'Level 11'), (12, 'Level 12'), (13, 'Level 13'), (14, 'Level 14'), (15, 'Level 15')], default=1, help_text='User Level'),
        ),
    ]
