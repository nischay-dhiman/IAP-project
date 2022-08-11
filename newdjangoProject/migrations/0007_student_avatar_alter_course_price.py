# Generated by Django 4.0.4 on 2022-08-10 18:58

from django.db import migrations, models
import newdjangoProject.models
import newdjangoProject.validators


class Migration(migrations.Migration):

    dependencies = [
        ('newdjangoProject', '0006_course_interested_course_stages'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='avatar',
            field=models.ImageField(default=1, upload_to=newdjangoProject.models.directory_path),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[newdjangoProject.validators.validate_price]),
        ),
    ]