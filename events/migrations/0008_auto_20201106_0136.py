# Generated by Django 3.1.3 on 2020-11-05 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_route'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='participant',
            field=models.ManyToManyField(blank=True, related_name='route', to='events.Participant'),
        ),
    ]
