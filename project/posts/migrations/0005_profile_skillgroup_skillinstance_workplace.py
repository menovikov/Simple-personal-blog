# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-09 22:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_draft'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('occupation', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('university', models.CharField(max_length=150)),
                ('faculty', models.CharField(max_length=100)),
                ('grad_years', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SkillGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SkillInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75)),
                ('level', models.CharField(max_length=50)),
                ('experience_time', models.CharField(max_length=50)),
                ('skill_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.SkillGroup')),
            ],
        ),
        migrations.CreateModel(
            name='WorkPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=50)),
                ('project', models.CharField(max_length=100)),
                ('corp_title', models.CharField(max_length=100)),
                ('start_end_dates', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('owner', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='posts.Profile')),
            ],
        ),
    ]
