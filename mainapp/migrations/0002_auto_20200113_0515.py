# Generated by Django 2.2 on 2020-01-13 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refundrequestmodel',
            name='order_number',
        ),
        migrations.AlterField(
            model_name='refundrequestmodel',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]