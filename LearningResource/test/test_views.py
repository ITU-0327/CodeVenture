import pytest
from django.urls import reverse
from django.test import RequestFactory, Client
from django.contrib.auth.models import AnonymousUser, User
from django.http import Http404

from LearningResource.views import lecture_view
from LearningResource.models import SubModule, LearningModule, VideoTutorial

from ProgressTracker.models import ProgressTracker, ModuleProgress
from UserManagement.models import Student


# Fixtures
@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='john', password='johnpassword')


@pytest.fixture
def student(user):
    return Student.objects.create(user=user)


@pytest.fixture
def client(db, user):
    c = Client()
    c.force_login(user)
    return c


@pytest.fixture
def progress_tracker(student):
    progress, _ = ProgressTracker.objects.get_or_create(student=student)
    return progress


@pytest.fixture
def learning_module(db):
    return LearningModule.objects.create(name="Test Module", short_name="TM", description="Test Module Desc")


@pytest.fixture
def video_tutorial(db):
    return VideoTutorial.objects.create(name="Test Video", video_id="12345678901")


@pytest.fixture
def sub_module(learning_module, video_tutorial):
    return SubModule.objects.create(name="Test Submodule", parent_module=learning_module, video=video_tutorial, difficulty_level="Basic", description="Test Desc")


# Test lecture_view
@pytest.mark.django_db
def test_lecture_view_with_valid_submodule_id(client, learning_module, video_tutorial, sub_module):
    response = client.get(reverse('lecture_view', args=[sub_module.id]))

    assert response.status_code == 200
    assert 'submodule' in response.context
    assert response.context['submodule'] == sub_module


@pytest.mark.django_db
def test_lecture_view_with_invalid_submodule_id(request_factory, user):
    request = request_factory.get(reverse('lecture_view', args=[9999]))
    request.user = user

    with pytest.raises(Http404, match="Submodule not found"):
        lecture_view(request, 9999)


@pytest.mark.django_db
def test_lecture_view_with_invalid_completed_submodule_id(request_factory, user, sub_module):
    # Set the submodule_id to a valid submodule but the complete_current value to an invalid ID (9999 in this case).
    request = request_factory.get(reverse('lecture_view', args=[sub_module.id]) + '?complete_current=9999')
    request.user = user

    with pytest.raises(Http404, match="Completed submodule not found"):
        lecture_view(request, sub_module.id)


@pytest.mark.django_db
def test_lecture_view_without_authentication(request_factory, sub_module):
    request = request_factory.get(reverse('lecture_view', args=[sub_module.id]))
    request.user = AnonymousUser()

    response = lecture_view(request, sub_module.id)

    assert response.status_code == 302
    assert reverse('login') in response.url


@pytest.mark.django_db
def test_complete_submodule(request_factory, user, student, progress_tracker, learning_module, video_tutorial, sub_module):
    request = request_factory.get(reverse('lecture_view', args=[sub_module.id]) + '?complete_current=' + str(sub_module.id))
    request.user = user

    response = lecture_view(request, sub_module.id)

    module_progress = ModuleProgress.objects.get(progress_tracker=progress_tracker, module=learning_module)
    assert module_progress.completed_submodules.filter(id=sub_module.id).exists()


# Test concept_module_view
@pytest.mark.django_db
def test_concept_module_view_response(client, student, progress_tracker):
    response = client.get(reverse('concept_modules'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_concept_module_view_unauthenticated(user):
    c = Client()
    response = c.get(reverse('concept_modules'))

    assert response.status_code == 302
    assert reverse('login') in response.url


@pytest.mark.django_db
def test_concept_module_view_template(client, student, progress_tracker):
    response = client.get(reverse('concept_modules'))
    assert 'ConceptModulesPage.html' in [template.name for template in response.templates]


# Test module_view
@pytest.mark.django_db
def test_module_view_unauthenticated(user):
    c = Client()
    response = c.get(reverse('learning_modules'))

    assert response.status_code == 302
    assert reverse('login') in response.url

