# Generated by Django 5.0.6 on 2024-06-25 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_remark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]