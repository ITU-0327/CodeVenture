from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import ModuleProgress, ProgressTracker
from UserManagement.models import Student


@receiver(m2m_changed, sender=ModuleProgress.completed_submodules.through)
def update_module_progress(sender, instance, **kwargs):
    instance.update_progress()
    instance.progress_tracker.update_overall_progress()


@receiver(post_save, sender=ModuleProgress)
def update_overall_progress_on_save(sender, instance, **kwargs):
    instance.progress_tracker.update_overall_progress()


@receiver(post_save, sender=Student)
def create_progress_tracker(sender, instance, created, **kwargs):
    if created:
        ProgressTracker.objects.create(student=instance)
