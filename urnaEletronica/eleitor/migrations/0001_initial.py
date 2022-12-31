# Generated by Django 4.1.4 on 2022-12-30 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('urna', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Eleitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('data_nascimento', models.DateField()),
                ('titulo_eleitor', models.CharField(max_length=12)),
                ('zona', models.CharField(max_length=4)),
                ('secao', models.CharField(max_length=4)),
                ('municipio', models.CharField(max_length=100)),
                ('uf', models.CharField(max_length=2)),
                ('data_emissao', models.DateField()),
                ('urna', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='eleitores', to='urna.urna')),
            ],
        ),
    ]