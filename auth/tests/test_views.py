from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APITestCase
from rest_framework import status
from allauth.account.models import EmailConfirmation

from accounts import models


class RegistrationTests(APITestCase):

    def setUp(self):
        password = get_random_string(10)
        self.registration_data = {
            'email': 'test@test.com',
            'first_name': 'test first name',
            'last_name': 'test last name',
            'password1': password,
            'password2': password,
        }

    def test_no_data(self):
        response = self.client.post(reverse('register'))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        for field in self.registration_data.keys():
            assert field in response.data
            assert response.data[field][0] == 'This field is required.'

    def test_wrong_email_format(self):
        data = {'email': 'some_wrong_email'}
        response = self.client.post(reverse('register'), data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['email'][0] == 'Enter a valid email address.'

    def test_to_long_first_name(self):
        self.registration_data.update({
            'first_name': get_random_string(length=51),
            'last_name': get_random_string(length=51),
        })
        response = self.client.post(reverse('register'), data=self.registration_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['first_name'][0] == 'Ensure this field has no more than 50 characters.'
        assert response.data['last_name'][0] == 'Ensure this field has no more than 50 characters.'

    def test_password_not_the_same(self):
        self.registration_data.update({'password2': get_random_string(11)})
        response = self.client.post(reverse('register'), data=self.registration_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'][0] == "The two password fields didn't match."

    def test_email_already_exist(self):
        models.User.objects.create(email=self.registration_data['email'])
        response = self.client.post(reverse('register'), data=self.registration_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['email'][0] == 'A user is already registered with this e-mail address.'

    def test_successfully_registration(self):
        response = self.client.post(reverse('register'), data=self.registration_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['detail'] == 'Verification e-mail sent.'

    def test_verify_email_wrong_code(self):
        data = {'key': 111111}
        response = self.client.post(reverse('account_email_verification_sent'), data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == 'Not found.'

    def test_verify_email_correct_code(self):
        response = self.client.post(reverse('register'), data=self.registration_data)
        assert response.status_code == status.HTTP_201_CREATED

        key = EmailConfirmation.objects.get(email_address__email=self.registration_data['email']).key
        response = self.client.post(reverse('account_email_verification_sent'), data={'key': key})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['detail'] == 'ok'


class LoginTests(APITestCase):
    def setUp(self):
        password = get_random_string(10)
        self.login_data = {
            'email': 'test@test.com',
            'password': password,
        }
        self.registration_data = {
            'email': 'test@test.com',
            'first_name': 'test first name',
            'last_name': 'test last name',
            'password1': password,
            'password2': password,
        }

    def test_wrong_email(self):
        response = self.client.post(reverse('login'), data=self.login_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'][0] == 'Unable to log in with provided credentials.'

    def test_empty_password(self):
        response = self.client.post(reverse('login'), data={'email': self.login_data['email']})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['password'][0] == 'This field is required.'

    def test_non_verified_email(self):
        self.client.post(reverse('register'), data=self.registration_data)
        response = self.client.post(reverse('login'), data=self.login_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'][0] == 'E-mail is not verified.'
