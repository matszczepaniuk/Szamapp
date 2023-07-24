from http import HTTPStatus
from unittest.mock import patch
import pytest
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import reverse
from django.test import TestCase
from Szamapp.views import *


class MainViewTest(TestCase):
    def test_mainview_url_accessible_by_name(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_mainview_uses_correct_template(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/main.html')

    def test_mainview_redirect_for_authenticated_user(self):
        User.objects.create_user(username='testuser1', password='testpassword1')
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('main'))
        assert response.status_code == 302
        assert response.url == reverse('step1')


class UserLoginViewTest(TestCase):
    def test_loginview_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_loginview_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/login.html')

    def test_loginview_post_valid(self):
        User.objects.create_user(username='testuser', password='testpassword')
        login_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(reverse('login'), login_data)
        assert response.status_code == 302
        assert response.url == reverse('step1')
        assert '_auth_user_id' in self.client.session

    def test_loginview_post_invalid(self):
        login_data = {
            'username': 'nonexistent_user',
            'password': 'wrong_password',
        }
        response = self.client.post(reverse('login'), login_data)
        assert response.status_code == 200
        assert '_auth_user_id' not in self.client.session


class RegistrationViewTest(TestCase):
    def test_registrationview_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_registrationview_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/registration.html')

    def test_registrationview_post_valid(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'testmail@gmail.com',
        }
        response = self.client.post(reverse('register'), data)
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('testpassword'))
        self.assertRedirects(response, reverse('login'))

    def test_registration_view_post_invalid(self):
        data = {
            'username': 'existing_user',
            'password1': 'testpassword',
            'password2': 'different_password',
        }
        self.client.post(reverse('register'), data)
        assert not User.objects.filter(username='existing_user', password='testpassword').exists()


class UserAccountViewTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_uses_correct_template(self):
        User.objects.create_user(username='testuser1', password='testpassword1')
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('account'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/account.html')


class AppStep1ViewTest(TestCase):
    def test_step1view_url_accessible_by_name(self):
        response = self.client.get(reverse('step1'))
        self.assertEqual(response.status_code, 200)

    def test_step1view_uses_correct_template(self):
        response = self.client.get(reverse('step1'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/step1.html')

    def test_step1view_post_valid(self):
        data = {
            'btn': 'Do 30 minut',
        }
        response = self.client.post(reverse('step1'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('step2'))
        self.assertIn('time', self.client.session)
        self.assertEqual(self.client.session['time'], 'Do 30 minut')

    def test_step1view_post_invalid(self):
        response = self.client.post(reverse('step1'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('time', self.client.session)


class AppStep2ViewTest(TestCase):
    def test_step2view_url_accessible_by_name(self):
        response = self.client.get(reverse('step2'))
        self.assertEqual(response.status_code, 200)

    def test_step2view_uses_correct_template(self):
        response = self.client.get(reverse('step2'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/step2.html')

    def test_step2view_post_valid(self):
        data = {
            'btn': 'Ziemniaki',
        }
        response = self.client.post(reverse('step2'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('step3'))
        self.assertIn('base', self.client.session)
        self.assertEqual(self.client.session['base'], 'Ziemniaki')

    def test_step2view_post_invalid(self):
        response = self.client.post(reverse('step2'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('base', self.client.session)


class AppStep3ViewTest(TestCase):
    def test_step3view_url_accessible_by_name(self):
        response = self.client.get(reverse('step3'))
        self.assertEqual(response.status_code, 200)

    def test_step3view_uses_correct_template(self):
        response = self.client.get(reverse('step3'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/step3.html')

    def test_step3view_post_valid(self):
        data = {
            'btn': 'Posiłek wegetariański',
        }
        response = self.client.post(reverse('step3'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('step4'))
        self.assertIn('type', self.client.session)
        self.assertEqual(self.client.session['type'], 'Posiłek wegetariański')

    def test_step3_view_post_invalid(self):
        response = self.client.post(reverse('step3'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('type', self.client.session)


class AppStep4ViewTest(TestCase):
    def test_step4view_url_accessible_by_name(self):
        response = self.client.get(reverse('step4'))
        self.assertEqual(response.status_code, 200)

    def test_step4view_uses_correct_template(self):
        response = self.client.get(reverse('step4'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/step4.html')

    def test_step4view_post_valid(self):
        data = {
            'ingredient1': 'Ingredient 1',
            'ingredient2': 'Ingredient 2',
            'ingredient3': 'Ingredient 3',
            'ingredient4': '',
            'ingredient5': '',
        }
        response = self.client.post(reverse('step4'), data)
        session = self.client.session
        assert 'ingredient1' in session
        assert session['ingredient1'] == 'Ingredient 1'
        assert 'ingredient2' in session
        assert session['ingredient2'] == 'Ingredient 2'
        assert 'ingredient3' in session
        assert session['ingredient3'] == 'Ingredient 3'
        assert Ingredient.objects.filter(name='Ingredient 1').exists()
        assert Ingredient.objects.filter(name='Ingredient 2').exists()
        assert Ingredient.objects.filter(name='Ingredient 3').exists()
        assert response.status_code == 302
        self.assertEqual(response["Location"], "/step5/")

    def test_step4view_post_invalid(self):
        data = {
            'ingredient1': 'Ingredient 1',
            'ingredient2': '',
            'ingredient3': '',
            'ingredient4': '',
            'ingredient5': '',
        }
        response = self.client.post(reverse('step4'), data)
        assert response.status_code == 200
        assert 'Musisz podać dwa składniki' in response.content.decode('utf-8')


@patch('openai.ChatCompletion.create')
def test_chat_meal_offers_view(mock_openai_create, client):
    data = {
        'time': 'Do 30 minut',
        'base': 'Ryż',
        'type': 'Danie wegańskie',
        'ingredient1': 'pomidor',
        'ingredient2': 'ogórek',
        'ingredient3': 'grzyby',
        'ingredient4': '',
        'ingredient5': '',
    }
    session = SessionStore()
    for key, value in data.items():
        session[key] = value
    session.save()
    mock_openai_create.return_value.choices[0].message["content"] = "1. Meal A. Meal B. Meal C."
    response = ChatMealOffers(client)
    session = client.session
    assert 'first_response' in session
    assert session['first_response'] == "1. Meal A. Meal B. Meal C."
    assert response.status_code == 302
    assert response.url == reverse('step5')


class AppStep5ViewTest(TestCase):
    def test_step5view_post_first_meal(self):
        data = {
            'first_meal': 'Meal A',
            'second_meal': 'Meal B',
            'third_meal': 'Meal C',
        }
        session = self.client.session
        for key, value in data.items():
            session[key] = value
        session.save()
        response = self.client.post(reverse('step5'), {'first_meal': ''})
        session = self.client.session
        assert 'choice' in session
        assert session['choice'] == 'Meal A'
        assert response.status_code == 302
        self.assertEqual(response["Location"], "/step6/")

    def test_step5view_post_second_meal(self):
        data = {
            'first_meal': 'Meal B',
            'second_meal': 'Meal B',
            'third_meal': 'Meal C',
        }
        session = self.client.session
        for key, value in data.items():
            session[key] = value
        session.save()
        response = self.client.post(reverse('step5'), {'second_meal': ''})
        session = self.client.session
        assert 'choice' in session
        assert session['choice'] == 'Meal B'
        assert response.status_code == 302
        self.assertEqual(response["Location"], "/step6/")

    def test_step5view_post_invalid(self):
        data = {
            'first_meal': 'Meal B',
            'second_meal': 'Meal B',
            'third_meal': 'Meal C',
        }
        session = self.client.session
        for key, value in data.items():
            session[key] = value
        session.save()
        response = self.client.post(reverse('step5'), {'invalid_button': ''})
        session = self.client.session
        assert 'choice' not in session


@patch('openai.ChatCompletion.create')
def test_chat_instructions_view(mock_openai_create, client):
    data = {
        'choice': 'Test Meal',
    }
    session = SessionStore()
    for key, value in data.items():
        session[key] = value
    session.save()
    mock_openai_create.return_value.choices[0].message["content"] = "Przepis dla dania Test Meal: Składniki... Instrukcje..."
    response = ChatInstructions(client)
    session = client.session
    assert 'second_response' in session
    assert session['second_response'] == "Przepis dla dania Test Meal: Składniki... Instrukcje..."
    assert response.status_code == 302
    assert response.url == reverse('step6')


class AppStep6ViewTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('step6'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('step6'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/step6.html')

    def test_app_step6_view_post_save(self):
        User.objects.create_user(username='testuser1', password='testpassword1')
        self.client.login(username='testuser1', password='testpassword1')
        data = {
            'choice': 'Test Recipe',
            'second_response': 'Recipe instructions...',
        }
        session = self.client.session
        for key, value in data.items():
            session[key] = value
        session.save()
        response = self.client.post(reverse('step6'), {'save': ''})
        assert response.status_code == 302
        assert Recipe.objects.filter(name='Test Recipe').exists()
        current_user = User.objects.get(username='testuser1')
        assert FavouriteRecipes.objects.filter(name='Test Recipe', user=current_user.id).exists()
        assert response.url == reverse('account')

    def test_app_step6_view_post_exit(self):
        response = self.client.post(reverse('step6'), {'exit': ''})
        assert response.status_code == 302
        assert response.url == reverse('main')
