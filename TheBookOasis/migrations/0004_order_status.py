# Generated by Django 4.1.7 on 2023-06-17 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TheBookOasis', '0003_alter_shoppingcart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Processing', 'Се процесира'), ('Deliver', 'Испратена на адреса')], default=1, max_length=100),
            preserve_default=False,
        ),
    ]
