# Generated by Django 3.2.7 on 2021-09-13 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0018_alter_leave_request_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]
