# Generated by Django 3.1.3 on 2023-11-20 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Final', '0011_auto_20231120_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='publicationNumber',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
