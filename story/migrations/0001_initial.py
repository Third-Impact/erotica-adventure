# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-03 02:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_text', models.TextField()),
                ('closed', models.BooleanField(default=True)),
                ('end_point', models.BooleanField(default=False)),
                ('save_point', models.BooleanField(default=False)),
                ('picture', models.URLField(blank=True)),
                ('last_edited', models.DateTimeField(verbose_name='last changed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='from_scene',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_scene', to='story.Scene'),
        ),
        migrations.AddField(
            model_name='branch',
            name='to_scene',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_scene', to='story.Scene'),
        ),
    ]
