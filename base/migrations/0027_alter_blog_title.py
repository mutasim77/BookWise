# Generated by Django 4.1.6 on 2023-05-13 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(help_text='The title of the blog', max_length=150),
        ),
    ]
