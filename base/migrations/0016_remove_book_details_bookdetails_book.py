# Generated by Django 4.1.6 on 2023-05-10 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_remove_bookdetails_book_alter_book_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='details',
        ),
        migrations.AddField(
            model_name='bookdetails',
            name='book',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.book'),
        ),
    ]
