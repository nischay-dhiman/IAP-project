# Generated by Django 4.0.4 on 2022-06-27 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newdjangoProject', '0003_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='newdjangoProject.student'),
        ),
        migrations.AddField(
            model_name='tag',
            name='topic',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='newdjangoProject.topic'),
        ),
    ]
