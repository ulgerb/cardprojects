# Generated by Django 4.1.4 on 2022-12-16 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appMy', '0003_category_alter_card_date_now'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appMy.category', verbose_name='Kategori'),
        ),
    ]
