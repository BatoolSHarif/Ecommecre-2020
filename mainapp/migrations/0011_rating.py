# Generated by Django 2.2 on 2020-01-18 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_checkoutmodel_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indRating', models.IntegerField(choices=[(1, 'Poor'), (2, 'Average'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')])),
                ('productID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.OrderItemModel')),
            ],
        ),
    ]