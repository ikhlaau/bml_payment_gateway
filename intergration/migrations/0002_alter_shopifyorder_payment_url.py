# Generated by Django 4.2.6 on 2024-06-14 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intergration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopifyorder',
            name='payment_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
