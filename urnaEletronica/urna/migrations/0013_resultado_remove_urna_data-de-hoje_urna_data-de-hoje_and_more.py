# Generated by Django 4.1.4 on 2023-01-31 00:09

import datetime
from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('urna', '0012_urna_data-de-hoje'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votos_invalidos', models.IntegerField()),
                ('votos_validos', models.IntegerField()),
                ('total_votos', models.IntegerField()),
                ('votos_candidato_A', models.IntegerField()),
                ('votos_candidato_B', models.IntegerField()),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='urna',
            name='data-de-hoje',
        ),
        migrations.AddConstraint(
            model_name='urna',
            constraint=models.CheckConstraint(check=models.Q(('data_votacao', datetime.date(2023, 1, 31))), name='data-de-hoje'),
        ),
        migrations.AddConstraint(
            model_name='resultado',
            constraint=models.CheckConstraint(check=models.Q(('total_votos', django.db.models.expressions.CombinedExpression(models.F('votos_validos'), '+', models.F('votos_invalidos')))), name='total_votos'),
        ),
        migrations.AddConstraint(
            model_name='resultado',
            constraint=models.CheckConstraint(check=models.Q(('votos_validos', django.db.models.expressions.CombinedExpression(models.F('votos_candidato_A'), '+', models.F('votos_candidato_B')))), name='votos_validos'),
        ),
    ]