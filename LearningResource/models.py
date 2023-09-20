from django.db import models


class VideoTutorial(models.Model):
    name = models.CharField(max_length=50, default='')
    video_id = models.CharField(max_length=11, null=True)
    # duration = models.IntegerField()

    def __str__(self):
        return self.name


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
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=50, unique=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name


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
    video = models.OneToOneField(VideoTutorial, on_delete=models.SET_NULL, null=True)
    prev_submodule = models.OneToOneField('SubModule', on_delete=models.SET_NULL, null=True, blank=True, related_name='prev_lecture')
    next_submodule = models.OneToOneField('SubModule', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_lecture')

    def __str__(self):
        return self.parent_module.short_name + ' - ' + self.name


class Badge(models.Model):
    name = models.CharField(max_length=50)
    icon_url = models.URLField()
    description = models.TextField()
