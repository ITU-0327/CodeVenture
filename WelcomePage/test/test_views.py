import pytest
from django.urls import reverse
from django.contrib.auth.models import User

from UserManagement.models import Student, Parent, Teacher
from WelcomePage.models import Ticket


# Fixture
@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def student(user):
    return Student.objects.create(user=user, profile_completed=False)


@pytest.fixture
def parent(user):
    return Parent.objects.create(user=user, profile_completed=False)


@pytest.fixture
def teacher(user):
    return Teacher.objects.create(user=user)


# Positive Tests
@pytest.mark.django_db
def test_unauthenticated_user_get_request(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'WelcomePage.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_unauthenticated_user_post_request(client):
    response = client.post(reverse('home'))
    assert response.status_code == 200
    assert 'WelcomePage.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_authenticated_student_complete_profile(client, student):
    student.profile_completed = True
    student.save()
    client.login(username='testuser', password='password')
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'MenuPage.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_authenticated_student_incomplete_profile(client, student):
    client.login(username='testuser', password='password')
    response = client.get(reverse('home'))
    assert response.status_code == 302  # Assuming the redirection happens due to incomplete profile
    assert response.url == reverse('choose_user_type')


@pytest.mark.django_db
def test_authenticated_parent_complete_profile(client, parent):
    parent.profile_completed = True
    parent.save()
    client.login(username='testuser', password='password')
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'MenuPage.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_authenticated_teacher(client, teacher):
    client.login(username='testuser', password='password')
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'MenuPage.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_valid_form_submission_authorized_creates_ticket(client, user):
    client.login(username='testuser', password='password')

    valid_data = {
        'fullname': 'John Doe',
        'subject': 'Test Subject',
        'message': 'This is a test message for ticket creation.',
    }

    response = client.post(reverse('home'), data=valid_data)

    # Ensure the ticket is saved in the database
    assert Ticket.objects.count() == 1
    ticket = Ticket.objects.first()
    assert ticket.user == user
    assert ticket.fullname == 'John Doe'
    assert ticket.subject == 'Test Subject'
    assert ticket.message == 'This is a test message for ticket creation.'

    # Ensure redirection happens after a successful form submission
    assert response.status_code == 302
    assert reverse('home') in response.url


@pytest.mark.skip(reason="Temporarily skipping due to haven't implemented")
@pytest.mark.django_db
def test_valid_form_submission_unauthorized_creates_ticket(client):
    valid_data = {
        'fullname': 'John Doe',
        'email': 'testing@example.com',
        'message': 'This is a test message for ticket creation.',
    }

    response = client.post(reverse('home'), data=valid_data)

    # Ensure the ticket is saved in the database
    assert Ticket.objects.count() == 1
    ticket = Ticket.objects.first()
    # assert ticket.user == user
    assert ticket.fullname == 'John Doe'
    assert ticket.email == 'testing@example.com'
    assert ticket.message == 'This is a test message for ticket creation.'

    # Ensure redirection happens after a successful form submission
    assert response.status_code == 302
    assert reverse('home') in response.url
