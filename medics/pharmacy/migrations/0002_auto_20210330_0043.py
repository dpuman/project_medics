# Generated by Django 2.2.10 on 2021-03-29 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.Pharmacy'),
        ),
    ]
