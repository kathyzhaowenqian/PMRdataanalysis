# Generated by Django 3.2 on 2023-09-07 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PMRKA', '0004_pmrresearchlistpmrka_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='pmrresearchlistpmrka',
            name='newold',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='业务类型'),
        ),
    ]
