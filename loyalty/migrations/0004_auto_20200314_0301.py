# Generated by Django 2.2.3 on 2020-03-14 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty', '0003_auto_20200314_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='file',
            field=models.FileField(upload_to='media'),
        ),
    ]