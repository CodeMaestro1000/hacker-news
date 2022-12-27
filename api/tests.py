from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model
from hackernews.models import Stories
from datetime import date
from rest_framework.test import APITestCase

# Create your tests here.
class APITest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.story = Stories.objects.create(
            id=1,
            title='user created test story',
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

    def testAPIListView(self):
        response = self.client.get('/api/v1/allstories/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'hacker news test story')

    def testStoryAPIListView(self):
        response = self.client.get('/api/v1/stories/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'user created test story')
        self.assertContains(response, 'hacker news test story')

    def testStoryAPIListView(self):
        response = self.client.get('/api/v1/userstories/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user created test story')
        self.assertNotContains(response, 'hacker news test story')

    def testJobStoryAPIListView(self):
        response = self.client.get('/api/v1/jobstories/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'user created test story')
        self.assertContains(response, 'hacker news test story')

    def testStoryCreateAPIView(self):
        data = {'username':self.user.username, 'password':'secret', 'title':'test post', 'text':'Lorem Ipsum doloret amet'}
        bad_data = {'username':self.user.username, 'password':'secret'}
        wrong_payload = {'username':self.user.username, 'password':'wrong password', 'title':'test post', 'text':'Lorem Ipsum doloret amet'}

        response = self.client.post('/api/v1/stories/new', data, format='json')
        bad_request = self.client.post('/api/v1/stories/new', bad_data, format='json')
        wrong_request = self.client.post('/api/v1/stories/new', wrong_payload, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(bad_request.status_code, 400)
        self.assertEqual(wrong_request.status_code, 401)
        # self.assertContains(wrong_request, 'Invalid User Credentials, Check username and password again')

    def testAPIGetItem(self):
        response = self.client.get('/api/v1/stories/item/1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'www.google.com')

    def testAPIUpdateItem(self):
        data = {'username':self.user.username, 'password':'secret', 'title':'Updated test post', 'text':'Updated'}
        permission_payload = {'username':self.user2.username, 'password':'secret', 'title':'test post', 'text':'Lorem Ipsum doloret amet'}
        wrong_payload = {'username':self.user.username, 'password':'wrong password', 'title':'test post', 'text':'Lorem Ipsum doloret amet'}

        response = self.client.put('/api/v1/stories/item/1', data, format='json')
        perm_response = self.client.put('/api/v1/stories/item/1', permission_payload, format='json')
        wrong_response = self.client.put('/api/v1/stories/item/1', wrong_payload, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(perm_response.status_code, 403)
        self.assertEqual(wrong_response.status_code, 401)
        self.assertContains(response, 'Updated test post')

    def testAPIDeleteItem(self):
        data = {'username':self.user.username, 'password':'secret'}
        response = self.client.delete('/api/v1/stories/item/1', data, format='json')
        no_data_response = self.client.delete('/api/v1/stories/item/15', data, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(no_data_response.status_code, 404)