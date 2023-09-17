from django.db import models


class LearningModule(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


class SubModule(models.Model):
    DIFFICULTY_CHOICES = [
        ('Basic', 'Basic'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=50)
    parent_module = models.ForeignKey(LearningModule, related_name='sub_modules', on_delete=models.CASCADE)
    difficulty_level = models.CharField(
        max_length=15,
        choices=DIFFICULTY_CHOICES,
        default='Basic'
    )
    description = models.TextField()


class VideoTutorial(models.Model):
    video_url = models.URLField()
    duration = models.IntegerField()
    subtitles = models.TextField()


class Challenge(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    hints = models.JSONField()
    solution_code = models.TextField()


class Quiz(models.Model):
    name = models.CharField(max_length=50)


class Question(models.Model):
    text = models.TextField()
    choices = models.JSONField()
    correct_answer = models.CharField(max_length=100)


class Badge(models.Model):
    name = models.CharField(max_length=50)
    icon_url = models.URLField()
    description = models.TextField()
