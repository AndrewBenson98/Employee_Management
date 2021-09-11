# Generated by Django 3.2.7 on 2021-09-08 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_auto_20210908_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='deptName',
            field=models.CharField(max_length=25, null=True, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='deptID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.department', verbose_name='department'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='empID',
            field=models.CharField(max_length=5, unique=True, verbose_name='Employee ID'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='fName',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hireDate',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Date joined'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='lName',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='last name'),
        ),
    ]
