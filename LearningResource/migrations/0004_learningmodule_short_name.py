# Generated by Django 4.2.5 on 2023-09-19 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LearningResource", "0003_alter_learningmodule_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="learningmodule",
            name="short_name",
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]