# Generated by Django 5.0 on 2024-11-29 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0004_remove_answer_answer_remove_answer_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='confirmation',
            field=models.ImageField(blank=True, null=True, upload_to='ww_confirmation/'),
        ),
    ]
