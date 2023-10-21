import pytest
from django.contrib.auth.models import User
from LearningResource.models import SubModule, LearningModule
from UserManagement.models import Student, Teacher, Parent
from ProgressTracker.models import ProgressTracker, ModuleProgress

from django.core.exceptions import ValidationError


# Fixtures
@pytest.fixture
def user():
    return User.objects.create_user('testuser', 'test@email.com', 'testpassword')


@pytest.fixture
def student(user):
    return Student.objects.create(user=user)


@pytest.fixture
def teacher(user):
    return Teacher.objects.create(user=user)


@pytest.fixture
def parent(user):
    return Parent.objects.create(user=user)


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


@pytest.fixture
def progress_tracker(student):
    progress, _ = ProgressTracker.objects.get_or_create(student=student)
    return progress


@pytest.fixture
def module_progress(progress_tracker, learning_module, sub_module):
    mp = ModuleProgress.objects.create(progress_tracker=progress_tracker, module=learning_module)
    mp.completed_submodules.add(sub_module)
    mp.update_progress()
    return mp


# Positive Tests
@pytest.mark.django_db
def test_create_student(student):
    assert student is not None
    assert student.user.username == 'testuser'
    assert student.profile_completed == False


@pytest.mark.django_db
def test_create_teacher(teacher):
    assert teacher is not None
    assert teacher.user.username == 'testuser'


@pytest.mark.django_db
def test_create_parent(parent):
    assert parent is not None
    assert parent.user.username == 'testuser'
    assert parent.profile_completed == False


@pytest.mark.django_db
def test_parent_get_children(parent, student):
    student.parent = parent
    student.save()
    children = parent.get_children()
    assert children.count() == 1
    assert children.first().user.username == 'testuser'


# Negative Tests
@pytest.mark.django_db
def test_invalid_student_birthday(user):
    with pytest.raises(ValidationError):
        Student.objects.create(user=user, birthday="invalid_date")


@pytest.mark.skip(reason="Temporarily skipping due to haven't implemented")
@pytest.mark.django_db
def test_invalid_parent_email(user):
    with pytest.raises(ValidationError):
        Student.objects.create(user=user, parent_email="invalid_email")


@pytest.mark.django_db
def test_student_str_representation(student):
    assert str(student) == student.user.username


@pytest.mark.django_db
def test_teacher_str_representation(teacher):
    assert str(teacher) == teacher.user.username


@pytest.mark.django_db
def test_parent_str_representation(parent):
    assert str(parent) == parent.user.username


@pytest.mark.django_db
def test_teacher_get_students(teacher, student, learning_module, module_progress):
    teacher.course.add(learning_module)
    teacher.save()

    assert teacher.get_students().count() == 1
    assert teacher.get_students().first().user.username == student.user.username
