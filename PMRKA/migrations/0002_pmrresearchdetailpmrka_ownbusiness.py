# Generated by Django 3.2 on 2023-09-07 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PMRKA', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pmrresearchdetailpmrka',
            name='ownbusiness',
            field=models.BooleanField(choices=[(True, '是'), (False, '否')], default=False, verbose_name='是否我司业务'),
        ),
    ]
