# Generated by Django 4.1.4 on 2023-01-29 15:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urna', '0003_urna_hora_fim_limite_urna_hora_inicio_limite'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='urna',
            name='data-de-hoje',
        ),
        migrations.AddConstraint(
            model_name='urna',
            constraint=models.CheckConstraint(check=models.Q(('data_votacao', datetime.date(2023, 1, 29))), name='data-de-hoje'),
        ),
    ]