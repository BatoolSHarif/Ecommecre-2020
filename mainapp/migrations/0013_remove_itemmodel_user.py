# Generated by Django 2.2 on 2020-01-21 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_producttags_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemmodel',
            name='user',
        ),
    ]
