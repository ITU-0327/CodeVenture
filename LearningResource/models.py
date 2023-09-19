from django.db import models


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
    deadline = models.DateTimeField(null=True, blank=True)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    choices = models.JSONField()
    correct_answer = models.CharField(max_length=100)


class LearningModule(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class SubModule(models.Model):
    DIFFICULTY_CHOICES = [
        ('Basic', 'Basic'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=50, unique=True)
    parent_module = models.ForeignKey(LearningModule, related_name='sub_modules', on_delete=models.CASCADE, null=True, blank=True)
    difficulty_level = models.CharField(
        max_length=15,
        choices=DIFFICULTY_CHOICES,
        default='Basic'
    )
    description = models.TextField()

    def __str__(self):
        return self.name


class Badge(models.Model):
    name = models.CharField(max_length=50)
    icon_url = models.URLField()
    description = models.TextField()
