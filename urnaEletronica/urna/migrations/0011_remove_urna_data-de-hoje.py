# Generated by Django 4.1.4 on 2023-01-30 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urna', '0010_alter_urna_data_votacao_alter_urna_hora_fim_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='urna',
            name='data-de-hoje',
        ),
    ]
