# Generated by Django 3.2 on 2023-04-17 06:47

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Marketing_Research_ZS', '0006_auto_20230404_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gsmrresearchlist',
            name='salesmode',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('我司业务:', (('代理', '代理'),)), ('第二类：非我司业务:', (('竞品', '竞品'), ('空白市场', '空白市场')))], max_length=25, null=True, verbose_name='销售模式(可多选)'),
        ),
    ]
