# Generated by Django 5.2.2 on 2025-06-05 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnessclass',
            name='name',
            field=models.CharField(choices=[('Yoga', 'Yoga'), ('Zumba', 'Zumba'), ('HIIT', 'HIIT')], max_length=50),
        ),
    ]
