# Generated by Django 4.1.3 on 2022-12-27 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_rename_prretnum_prretynum'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PrretyNum',
            new_name='PrettyNum',
        ),
    ]
