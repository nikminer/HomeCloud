# Generated by Django 2.1.7 on 2019-03-22 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PublicFile',
            fields=[
                ('pseudoname', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('path', models.URLField(max_length=100000)),
                ('isvisible', models.BooleanField(default=False)),
            ],
        ),
    ]