import pytest
from django.contrib.auth.models import User

from UserManagement.models import Student
from ProgressTracker.models import ProgressTracker, ModuleProgress
from LearningResource.models import LearningModule, SubModule


# Fixture
@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def student(user):
    return Student.objects.create(user=user, profile_completed=False)


@pytest.fixture
def learning_module():
    return LearningModule.objects.create(name="Django Basics", short_name="DJ-Basics", description="Intro to Django")


@pytest.fixture
def sub_module(learning_module):
    return SubModule.objects.create(
        name="Setup",
        parent_module=learning_module,
        description="Setting up Django",
    )


# Positive Tests
@pytest.mark.django_db
def test_progress_tracker_string_representation(student):
    tracker = ProgressTracker.objects.get(student=student)
    expected_str = f"{student.user.username} - 0.0%"
    assert str(tracker) == expected_str


@pytest.mark.django_db
def test_progress_tracker_no_modules_sets_zero_progress(student):
    tracker = ProgressTracker.objects.get(student=student)
    tracker.update_overall_progress()
    assert tracker.overall_progress == 0


@pytest.mark.django_db
def test_module_progress_is_completed(student, learning_module):
    tracker = ProgressTracker.objects.get(student=student)
    module_progress = ModuleProgress.objects.create(progress_tracker=tracker, module=learning_module, progress=1)
    assert module_progress.is_completed()

    module_progress.progress = 0.5
    module_progress.save()
    assert not module_progress.is_completed()


@pytest.mark.django_db
def test_module_progress_string_representation(student, learning_module):
    tracker = ProgressTracker.objects.get(student=student)
    module_progress = ModuleProgress.objects.create(progress_tracker=tracker, module=learning_module, progress=0.5)
    expected_str = f"{tracker.student.user.username} - {learning_module.name} - 50.0%"
    assert str(module_progress) == expected_str


@pytest.mark.django_db
def test_module_progress_no_submodules_sets_zero_progress(student, learning_module):
    tracker = ProgressTracker.objects.get(student=student)
    module_progress = ModuleProgress.objects.create(progress_tracker=tracker, module=learning_module)
    module_progress.update_progress()
    assert module_progress.progress == 0


@pytest.mark.django_db
def test_module_progress_current_submodule(student, learning_module, sub_module):
    tracker = ProgressTracker.objects.get(student=student)
    module_progress = ModuleProgress.objects.create(progress_tracker=tracker, module=learning_module)

    assert module_progress.current_submodule() == sub_module

    # Add the submodule to completed and check again
    module_progress.add_completed_submodule(sub_module)
    assert module_progress.current_submodule() is None
