# Generated by Django 4.2.4 on 2023-08-14 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poetry_translation', '0006_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poem',
            name='language_engine',
            field=models.CharField(choices=[('GoogleTranslator', 'Google Translator'), ('ChatGptTranslator', 'ChatGPT Translator'), ('ChatGpt_Bot', 'ChatGPT Poet')], max_length=30),
        ),
        migrations.AlterField(
            model_name='poem',
            name='source_lang',
            field=models.CharField(choices=[('auto', 'Detect language'), ('english', 'English'), ('russian', 'Russian'), ('spanish', 'Spanish'), ('italian', 'Italian'), ('french', 'French'), ('german', 'German'), ('hindi', 'Hindi'), ('arabic', 'Arabic'), ('portuguese', 'Portuguese'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('chinese (simplified)', 'Chinese Simplified'), ('chinese (traditional)', 'Chinese Traditional'), ('turkish', 'Turkish'), ('indonesian', 'Indonesian')], max_length=30),
        ),
        migrations.AlterField(
            model_name='poem',
            name='target_lang',
            field=models.CharField(choices=[('auto', 'Detect language'), ('english', 'English'), ('russian', 'Russian'), ('spanish', 'Spanish'), ('italian', 'Italian'), ('french', 'French'), ('german', 'German'), ('hindi', 'Hindi'), ('arabic', 'Arabic'), ('portuguese', 'Portuguese'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('chinese (simplified)', 'Chinese Simplified'), ('chinese (traditional)', 'Chinese Traditional'), ('turkish', 'Turkish'), ('indonesian', 'Indonesian')], max_length=30),
        ),
    ]
