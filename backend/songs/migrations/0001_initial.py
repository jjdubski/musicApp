# Generated by Django 5.1.6 on 2025-03-01 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trackID', models.CharField(max_length=100, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('artist', models.CharField(max_length=100)),
                ('album', models.CharField(max_length=100)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('genre', models.CharField(max_length=50)),
                ('image', models.URLField(blank=True)),
            ],
        ),
    ]
