# Generated by Django 5.0.6 on 2024-07-01 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('essay', '0003_rename_updatatime_essay_updatetime_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='essay',
            old_name='typeid',
            new_name='typedata',
        ),
    ]
