# Generated by Django 4.1.6 on 2023-05-10 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_alter_bookdetails_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookDetails',
        ),
    ]
