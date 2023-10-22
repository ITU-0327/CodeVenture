import pytest
from django.urls import reverse
from django.test import RequestFactory
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404

from UserManagement.views import register_user
from UserManagement.models import Student, Parent, Teacher
from UserManagement.forms import StudentCreationForm, ParentCreationForm


# Fixtures
@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def user():
    return User.objects.create_user('testuser', 'test@email.com', 'testpassword')


@pytest.fixture
def student_user():
    return User.objects.create_user('studentuser', 'student@email.com', 'testpassword')


@pytest.fixture
def parent_user():
    return User.objects.create_user('parentuser', 'parent@email.com', 'testpassword')


@pytest.fixture
def teacher_user():
    return User.objects.create_user('teacheruser', 'teacher@email.com', 'testpassword')


@pytest.fixture
def student(student_user):
    return Student.objects.create(user=student_user)


@pytest.fixture
def parent(parent_user):
    return Parent.objects.create(user=parent_user)


@pytest.fixture
def teacher(teacher_user):
    return Teacher.objects.create(user=teacher_user)


@pytest.fixture
def client_authenticated(client, user):
    client.login(username="testuser", password="testpassword")
    return client


@pytest.fixture
def student_authenticated(client, student_user):
    client.login(username="studentuser", password="testpassword")
    return client


@pytest.fixture
def parent_authenticated(client, parent_user):
    client.login(username="parentuser", password="testpassword")
    return client


@pytest.fixture
def teacher_authenticated(client, teacher_user):
    client.login(username="teacheruser", password="testpassword")
    return client


# Positive Tests
# Test login_view
@pytest.mark.django_db
def test_login_view_with_valid_credentials(client, user):
    response = client.post(reverse('login'), data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_login_view_authenticated_user(client_authenticated):
    response = client_authenticated.get(reverse('login'))
    assert response.status_code == 302  # Expected redirect as the user is already logged in
    assert response.url == reverse('home')


# Test Logout
@pytest.mark.django_db
def test_logout_user(client_authenticated):
    response = client_authenticated.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('home')


# Test register_user
@pytest.mark.parametrize('user_type', ['student', 'parent', 'teacher'])
@pytest.mark.django_db
def test_register_user_valid_types(client, user_type):
    valid_form_data = {
        "username": "newuser",
        "password1": "complexpassword",
        "password2": "complexpassword",
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
    response = client.post(reverse('register_user', args=[user_type]), data=valid_form_data)
    assert response.status_code == 302  # Expected redirect to 'complete_profile'
    assert response.url == reverse('complete_profile')
    assert User.objects.filter(username="newuser").exists()

    # Further checking if the correct user type object is created
    if user_type == 'student':
        assert Student.objects.filter(user__username="newuser").exists()
    elif user_type == 'parent':
        assert Parent.objects.filter(user__username="newuser").exists()
    elif user_type == 'teacher':
        assert Teacher.objects.filter(user__username="newuser").exists()


# Tests complete_profile
@pytest.mark.django_db
def test_complete_profile_for_student_get_request(student_authenticated, student):
    response = student_authenticated.get(reverse('complete_profile'))
    assert response.status_code == 200
    assert isinstance(response.context['form'], StudentCreationForm)


@pytest.mark.django_db
def test_complete_profile_for_parent_get_request(parent_authenticated, parent):
    response = parent_authenticated.get(reverse('complete_profile'))
    assert response.status_code == 200
    assert isinstance(response.context['form'], ParentCreationForm)


@pytest.mark.django_db
def test_complete_profile_for_teacher_redirect(teacher_authenticated, teacher):
    response = teacher_authenticated.get(reverse('complete_profile'))
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_complete_profile_for_student_post_request_valid_data(student_authenticated, student):
    post_data = {
        'birthday': '2000-01-01',
        'coding_experience': 'No experience'
    }
    response = student_authenticated.post(reverse('complete_profile'), data=post_data)
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_complete_profile_for_children_adding_parent(student_authenticated, student, parent):
    post_data = {
        'parent_email': parent.user.email,
        'birthday': '2000-01-01',
        'coding_experience': 'No experience'
    }
    response = student_authenticated.post(reverse('complete_profile'), data=post_data)

    student.refresh_from_db()
    assert student.parent == parent


@pytest.mark.django_db
def test_complete_profile_for_parent_post_request_valid_data(parent_authenticated, parent, student):
    post_data = {
        'children_email': student.user.email
    }
    response = parent_authenticated.post(reverse('complete_profile'), data=post_data)

    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_complete_profile_for_parent_adding_children(parent_authenticated, parent, student):
    post_data = {
        'children_email': student.user.email
    }
    response = parent_authenticated.post(reverse('complete_profile'), data=post_data)

    student.refresh_from_db()
    assert student.parent == parent


# Test choose_user_type
def test_choose_user_type_response(client):
    response = client.get(reverse('choose_user_type'))
    assert response.status_code == 200
    assert 'SelectRoleForm.html' in [template.name for template in response.templates]


@pytest.mark.parametrize('user_type', ['student', 'parent', 'teacher'])
@pytest.mark.django_db
def test_choose_user_type_unauthenticated(client, user_type):
    post_data = {'role': user_type}
    response = client.post(reverse('choose_user_type'), data=post_data)
    assert response.status_code == 302
    assert response.url == reverse('register_user', args=[user_type])


@pytest.mark.parametrize('user_type', ['student', 'parent'])
@pytest.mark.django_db
def test_choose_user_type_authenticated_student_parent(client_authenticated, user, user_type):
    post_data = {'role': user_type}
    response = client_authenticated.post(reverse('choose_user_type'), data=post_data)
    assert response.status_code == 302
    assert response.url == reverse('complete_profile')
    assert hasattr(user, user_type)


@pytest.mark.django_db
def test_choose_user_type_authenticated_teacher(client_authenticated, user):
    post_data = {'role': 'teacher'}
    response = client_authenticated.post(reverse('choose_user_type'), data=post_data)
    assert response.status_code == 302
    assert response.url == reverse('home')
    assert hasattr(user, 'teacher')


@pytest.mark.parametrize('initial_user_type', ['student', 'parent', 'teacher'])
@pytest.mark.django_db
def test_choose_user_type_authenticated_switch_role(client_authenticated, initial_user_type, user):
    if initial_user_type == 'student':
        Student.objects.create(user=user)
    elif initial_user_type == 'parent':
        Parent.objects.create(user=user)
    elif initial_user_type == 'teacher':
        Teacher.objects.create(user=user)

    assert hasattr(user, initial_user_type)

    # Switch to a different role
    switch_roles = {
        'student': 'parent',
        'parent': 'teacher',
        'teacher': 'student'
    }
    post_data = {'role': switch_roles[initial_user_type]}
    response = client_authenticated.post(reverse('choose_user_type'), data=post_data)

    # Expect redirection based on chosen role
    expected_redirect = reverse('complete_profile') if post_data['role'] != 'teacher' else reverse('home')
    assert response.status_code == 302
    assert response.url == expected_redirect

    # Refresh user object from DB to get latest updates
    user.refresh_from_db()

    # Ensure initial role is removed and new role is assigned
    assert not hasattr(user, initial_user_type)
    assert hasattr(user, switch_roles[initial_user_type])


# Negative Tests
# Test login_view
@pytest.mark.django_db
def test_login_view_unauthenticated_user(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200  # Expected to see the login page
    assert 'login_register.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_login_view_without_username(client):
    response = client.post(reverse('login'), data={
        "password": "testpassword"
    })
    assert response.status_code == 200  # Expected the same page
    assert ("Both username and password must be provided."
            in [message.message for message in
                messages.get_messages(response.wsgi_request)])


@pytest.mark.django_db
def test_login_view_without_password(client):
    response = client.post(reverse('login'), data={
        "username": "testuser"
    })
    assert response.status_code == 200  # Expected the same page
    assert ("Both username and password must be provided."
            in [message.message for message in
                messages.get_messages(response.wsgi_request)])


@pytest.mark.django_db
def test_login_view_without_both_credentials(client):
    response = client.post(reverse('login'), data={})
    assert response.status_code == 200  # Expected the same page
    assert ("Both username and password must be provided."
            in [message.message for message in
                messages.get_messages(response.wsgi_request)])


@pytest.mark.django_db
def test_login_view_non_existing_user(client):
    response = client.post(reverse('login'), data={
        "username": "nonexistentuser",
        "password": "somepass"
    })
    assert response.status_code == 200  # Expected the same page due to the error
    assert "User does not exist" in [message.message for message in
                                     messages.get_messages(response.wsgi_request)]


@pytest.mark.django_db
def test_login_view_wrong_password(client, user):
    response = client.post(reverse('login'), data={
        "username": user.username,
        "password": "wrongpass"
    })
    assert response.status_code == 200
    assert 'Username or Password wrong.' in [message.message for message in
                                             messages.get_messages(response.wsgi_request)]


# Test register_user
@pytest.mark.django_db
def test_register_user_invalid_user_type(request_factory):
    request = request_factory.get(reverse('register_user', args=['invalidtype']))

    with pytest.raises(Http404, match="User Type not found"):
        register_user(request, 'invalidtype')


@pytest.mark.parametrize('user_type', ['student', 'parent', 'teacher'])
@pytest.mark.django_db
def test_register_user_invalid_form_data(client, user_type):
    invalid_form_data = {
        "username": "newuser",
        "password1": "short",
        "password2": "short",
        "email": "test@example.com"
    }
    response = client.post(reverse('register_user', args=[user_type]), data=invalid_form_data)
    assert response.status_code == 200  # Expected to stay on the same page due to form errors
    assert 'login_register.html' in [template.name for template in
                                     response.templates]  # Ensure we're on the registration page


# Tests complete_profile
@pytest.mark.django_db
def test_complete_profile_unauthenticated_user(client):
    response = client.get(reverse('complete_profile'))
    assert response.status_code == 302
    assert reverse('login') in response.url


@pytest.mark.django_db
def test_complete_profile_no_user_type_redirect(client_authenticated, user):
    response = client_authenticated.get(reverse('complete_profile'))
    assert response.status_code == 302
    assert response.url == reverse('choose_user_type')


@pytest.mark.django_db
def test_complete_profile_for_student_post_request_invalid_data(student_authenticated, student):
    post_data = {
        'birthday': '',
        'coding_experience': ''
    }
    response = student_authenticated.post(reverse('complete_profile'), data=post_data)
    assert response.status_code == 200
    assert "This field is required." in str(response.content)


@pytest.mark.django_db
def test_complete_profile_for_parent_invalid_child_email(parent_authenticated, parent):
    invalid_email = "nonexistentstudent@example.com"
    post_data = {
        'children_email': invalid_email
    }
    response = parent_authenticated.post(reverse('complete_profile'), data=post_data)
    assert response.status_code == 200
    assert f"No student found with the email: {invalid_email}" in [message.message for message in
                                                                   messages.get_messages(response.wsgi_request)]


@pytest.mark.django_db
def test_complete_profile_for_student_invalid_parent_email(student_authenticated, student):
    invalid_email = "nonexistentparent@example.com"
    post_data = {
        'birthday': '2000-01-01',
        'coding_experience': 'No experience',
        'parent_email': invalid_email
    }
    response = student_authenticated.post(reverse('complete_profile'), data=post_data)
    assert response.status_code == 200
    assert (f"No parent found with the email: {invalid_email}"
            in [message.message for message in messages.get_messages(response.wsgi_request)])
