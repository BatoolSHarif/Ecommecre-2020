# Generated by Django 2.2 on 2020-01-13 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_refundrequestmodel_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemmodel',
            name='item_type',
            field=models.CharField(choices=[('B', 'Beds'), ('D', 'Desks'), ('L', 'Lighting')], default='S', max_length=2),
        ),
    ]
