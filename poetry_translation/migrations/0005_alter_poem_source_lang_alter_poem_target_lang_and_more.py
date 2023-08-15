# Generated by Django 4.2.4 on 2023-08-14 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poetry_translation', '0004_alter_poem_language_engine_alter_poem_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poem',
            name='source_lang',
            field=models.CharField(choices=[('auto', 'Detect language'), ('english', 'English'), ('russian', 'Russian'), ('spanish', 'Spanish')], max_length=20),
        ),
        migrations.AlterField(
            model_name='poem',
            name='target_lang',
            field=models.CharField(choices=[('auto', 'Detect language'), ('english', 'English'), ('russian', 'Russian'), ('spanish', 'Spanish')], max_length=20),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_premium', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
