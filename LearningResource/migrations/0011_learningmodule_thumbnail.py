# Generated by Django 4.2.5 on 2023-10-20 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LearningResource", "0010_delete_challenge_delete_question_delete_quiz"),
    ]

    operations = [
        migrations.AddField(
            model_name="learningmodule",
            name="thumbnail",
            field=models.URLField(default="", null=True),
        ),
    ]
