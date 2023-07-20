from django.shortcuts import reverse
from django.test import TestCase


class MainViewTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/main.html')


class UserLoginViewTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/login.html')


class RegistrationViewTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/registration.html')


class UserAccountViewTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/account.html')


class AppStep1ViewTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('step1'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('step1'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/step1.html')


class AppStep2ViewTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('step2'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('step2'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/step2.html')


class AppStep3ViewTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('step3'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('step3'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/step3.html')


class AppStep4ViewTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('step4'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('step4'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/step4.html')


class AppStep5ViewTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('step5'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('step5'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/step5.html')


class AppStep6ViewTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('step6'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('step6'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/step6.html')
