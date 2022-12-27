from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Stories, Comments
from datetime import date

# Create your tests here.
class StoryTests(TestCase):
    def setUp(self):
        self.story = Stories.objects.create(
            id=1,
            title='test story',
            date_added=date.today(),
            author='john_doe',
            url='www.google.com',
            score=0,
            kids=False,
            story_type='story',
        )

        self.story2 = Stories.objects.create(
            id=2,
            title='hacker news test story',
            date_added=date.today(),
            author='jane_doe',
            url='www.google.com',
            score=0,
            kids=False,
            story_type='job',
            from_hn=True
        )

        self.user = get_user_model().objects.create_user(
            username='john_doe',
            email='test@email.com',
            password='secret'
        )

        self.user2 = get_user_model().objects.create_user(
            username='jane_doe',
            email='tes22t@email.com',
            password='secret'
        )

        self.comment = Comments.objects.create(
            story=self.story,
            id=1,
            parent_id=self.story.id,
            author='jane_doe',
            date_added=date.today(),
            text='true story'
        )

    def test_story_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test story')
        self.assertTemplateUsed(response, 'home.html')

    def test_story_detail_view(self):
        response = self.client.get('/story/1/')
        no_response = self.client.get('/story/04212/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'john_doe')
        self.assertContains(response, 'true story') # test if comment appears on page
        self.assertTemplateUsed(response, 'story_detail.html')

    def test_story_filter_view(self):
        response = self.client.get('/filters/?q=story/')
        no_response = self.client.get('/filters/?q=job/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 200)
        self.assertTemplateUsed(response, 'story_filter.html')
        self.assertTemplateUsed(no_response, 'story_filter.html')

    def test_user_story_list_view(self):
        response = self.client.login(username=self.user.username, password='secret')
        self.assertEqual(response, True)
        response = self.client.get('/mystories/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_story.html')

    def test_story_search_view(self):
        response = self.client.get('/search/?q=test story/')
        self.assertEqual(response.status_code, 200)

    def test_absolute_url(self):
        self.assertEqual(self.story.get_absolute_url(), '/story/1/')

    def test_story_update(self):
        response = self.client.login(username=self.user.username, password='secret')
        self.assertEqual(response, True)
        response = self.client.get('/story/1/edit/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('edit_story', args='1'), {
            'title': 'Updated title',
            'text': 'Updated text',
        })
        self.assertEqual(response.status_code, 302)
        no_response = self.client.get('/story/2/edit/')
        self.assertEqual(no_response.status_code, 403)
        self.client.logout()

        response = self.client.login(username=self.user2.username, password='secret')
        self.assertEqual(response, True)
        response = self.client.get('/story/1/edit/')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_story_delete(self):
        response = self.client.login(username=self.user2.username, password='secret')
        self.assertEqual(response, True)
        response = self.client.get('/story/1/delete/')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        response = self.client.login(username=self.user.username, password='secret')
        self.assertEqual(response, True)
        response = self.client.get('/story/1/delete/')
        self.assertEqual(response.status_code, 200)
        no_response = self.client.get('/story/2/delete/')
        self.assertEqual(no_response.status_code, 403)
        self.client.logout()
