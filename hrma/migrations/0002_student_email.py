# Generated by Django 4.0.2 on 2022-04-28 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrma', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.CharField(default='No email', max_length=60),
        ),
    ]