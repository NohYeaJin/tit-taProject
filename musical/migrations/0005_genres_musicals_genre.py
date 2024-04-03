# Generated by Django 5.0.3 on 2024-04-03 12:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musical', '0004_categories_locations_alter_musicals_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='musicals',
            name='genre',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='musical.genres'),
            preserve_default=False,
        ),
    ]
