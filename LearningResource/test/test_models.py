import pytest
from LearningResource.models import VideoTutorial, LearningModule, SubModule, Badge
from django.db import IntegrityError


@pytest.fixture
def video_tutorial():
    return VideoTutorial.objects.create(name="Sample Video", video_id="rHux0gMZ3Eg")


@pytest.fixture
def learning_module():
    return LearningModule.objects.create(name="Django Basics", short_name="DJ-Basics", description="Intro to Django")


@pytest.fixture
def sub_module(video_tutorial, learning_module):
    return SubModule.objects.create(
        name="Setup",
        parent_module=learning_module,
        description="Setting up Django",
        video=video_tutorial,
    )


@pytest.fixture
def badge():
    return Badge.objects.create(
        name="Django Novice",
        icon_url="https://example.com/badge.png",
        description="Earned after completing Django Basics",
    )


# VideoTutorial Tests
@pytest.mark.django_db
def test_video_tutorial_creation(video_tutorial):
    assert VideoTutorial.objects.count() == 1
    assert video_tutorial.name == "Sample Video"
    assert len(video_tutorial.video_id) == 11
    assert video_tutorial.video_id == "rHux0gMZ3Eg"


# LearningModule Tests
@pytest.mark.django_db
def test_learning_module_creation(learning_module):
    assert LearningModule.objects.count() == 1
    assert learning_module.name == "Django Basics"
    assert learning_module.short_name == "DJ-Basics"


@pytest.mark.django_db
def test_learning_module_name_uniqueness(learning_module):
    with pytest.raises(IntegrityError):
        LearningModule.objects.create(name="Django Basics", short_name="DJ-Advanced", description="Another Module")


@pytest.mark.django_db
def test_learning_module_thumbnail(learning_module):
    assert learning_module.thumbnail == ''  # Checking default value


# SubModule Tests
@pytest.mark.django_db
def test_sub_module_creation(sub_module):
    assert SubModule.objects.count() == 1
    assert sub_module.name == "Setup"
    assert sub_module.parent_module.name == "Django Basics"
    assert sub_module.difficulty_level == 'Basic'
    assert sub_module.video.name == "Sample Video"


@pytest.mark.django_db
def test_sub_module_relationships(learning_module, sub_module):
    assert learning_module.sub_modules.count() == 1
    assert learning_module.sub_modules.first().name == "Setup"


@pytest.mark.django_db
def test_sub_module_difficulty_choices(sub_module):
    assert sub_module.difficulty_level in dict(SubModule.DIFFICULTY_CHOICES).keys()


# Badge Tests
@pytest.mark.django_db
def test_badge_creation(badge):
    assert Badge.objects.count() == 1
    assert badge.name == "Django Novice"
