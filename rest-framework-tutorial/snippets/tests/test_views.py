from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

from snippets.models import Snippet
from snippets.views import SnippetViewSet
from snippets.serializers import SnippetSerializer

class ViewTestCase(APITestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="nerd")

        # if use django TestCase Initialize client  
        # self.client = APIClient()

        # force client to use authentication
        self.client.force_authenticate(user=user)

        self.snippet_data = {'code': 'balbaa', 'owner': user.id}
        self.response = self.client.post(
            reverse('snippet-list'),
            self.snippet_data,
            format="json")

    def test_login(self):
        user = User.objects.create(username="hero")
        self.client.login(username=user.username, password= user.password)
        response = self.client.get('/snippets/', follow=True)
        self.assertEqual(200, response.status_code)

    def test_api_can_create_a_snippet(self):
        """Test the api has snippet creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_is_enforced(self):
        """Test that the api has user authorization."""
        factory = APIRequestFactory()
        view = SnippetViewSet.as_view({'delete': 'destroy'})
        request = factory.delete('/snippets/')
        force_authenticate(request, user=None, token=None)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorization_is_not_enforced_in_snippets_list(self):
        """Test that the api has user authorization."""
        factory = APIRequestFactory()
        view = SnippetViewSet.as_view({'get': 'list'})
        request = factory.get('/snippets/')
        force_authenticate(request, user=None, token=None)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorization_is_enforced_in_snippets_update(self):
        """Test that the api has user authorization."""
        factory = APIRequestFactory()
        snippet = Snippet.objects.get(id=1)
        change_snippet = {'code': 'something new'}

        view = SnippetViewSet.as_view({'put': 'update'})
        request = factory.put('/snippets/', change_snippet)
        user = User.objects.get(username="nerd")
        force_authenticate(request, user=user)
        response = view(request, pk= snippet.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

