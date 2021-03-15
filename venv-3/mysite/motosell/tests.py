from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from . import views
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from .forms import LoginUserForm


class TestUrls(TestCase):
    def test_url_main(self):
        url = reverse('main')
        print(resolve(url))
        self.assertEquals(resolve(url).func, views.mainView)

    def test_url_login(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEquals(resolve(url).func, views.loginView)

    def test_url_register(self):
        url = reverse('signup')
        print(resolve(url))
        self.assertEquals(resolve(url).func, views.signupView)

    def test_url_logout(self):
        url = reverse('logout')
        print(resolve(url))
        self.assertEquals(resolve(url).func, views.logoutView)


class TestForms(SimpleTestCase):

    def test_login_form_validate_data_normal_case(self):
        form = LoginUserForm(data={
            'username': 'username1',
            'password': 'password1'
        })
        self.assertTrue(form.is_valid())

    def test_login_form_validate_data_max_case(self):
        form_max = LoginUserForm(data={
            'username': 'username11username11username11username11username111',
            'password': 'password1'
        })
        self.assertFalse(form_max.is_valid())

    def test_login_form_no_data(self):
        form = LoginUserForm(data={})
        self.assertFalse(form.is_valid())

    def test_login_form_required_fields(self):
        form = LoginUserForm(data={})
        self.assertEquals(len(form.errors), 2)  # form.errors - 2 pola 'wymagane' -> 2 błędy