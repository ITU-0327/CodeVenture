import pytest
from django.contrib.auth.models import User

from WelcomePage.models import Ticket


# Fixture
@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')


@pytest.mark.django_db
def test_ticket_string_representation(user):
    ticket = Ticket.objects.create(
        user=user,
        fullname="John Doe",
        subject="Test Subject",
        message="Test message"
    )
    assert str(ticket) == "John Doe - Test Subject"


@pytest.mark.django_db
def test_ticket_username_property(user):
    ticket = Ticket.objects.create(
        user=user,
        fullname="John Doe",
        subject="Test Subject",
        message="Test message"
    )
    assert ticket.username == "testuser"


@pytest.mark.django_db
def test_ticket_email_property(user):
    user.email = "testuser@example.com"
    user.save()
    ticket = Ticket.objects.create(
        user=user,
        fullname="John Doe",
        subject="Test Subject",
        message="Test message"
    )
    assert ticket.email == "testuser@example.com"
