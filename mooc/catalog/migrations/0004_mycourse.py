# Generated by Django 3.0.5 on 2020-04-28 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200416_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_accessed', models.DateField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('n', 'Not started'), ('i', 'Incomplete'), ('c', 'Completed')], default='n', help_text='Courses taken', max_length=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Course')),
            ],
        ),
    ]