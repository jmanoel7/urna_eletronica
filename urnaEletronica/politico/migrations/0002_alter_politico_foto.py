# Generated by Django 4.1.4 on 2022-12-30 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('politico', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='politico',
            name='foto',
            field=models.ImageField(height_field='128', upload_to='', width_field='128'),
        ),
    ]