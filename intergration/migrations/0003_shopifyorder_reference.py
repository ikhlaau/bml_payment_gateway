# Generated by Django 4.2.6 on 2024-06-14 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intergration', '0002_alter_shopifyorder_payment_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopifyorder',
            name='reference',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]