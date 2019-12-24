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

    fixtures = ['snippets.json', 'users.json']

    def setUp(self):
        """Define the test client and other test variables."""
      

    def test_snippet_serializer_code_validation(self):
        self.assertEqual(SnippetSerializer.validate_code(self,code='code1'), 'code1')

    def test_update_snippet_serializer(self,):
        snippet_dict = {
            'id': '1',
            'code': 'test2 ',
        }
        self.snippet = Snippet.objects.get(pk=1)
        snippet = SnippetSerializer(data=snippet_dict)
        snippet.is_valid()
        if snippet.validated_data:
            snippet = snippet.update(self.snippet, snippet.validated_data)
            self.assertIsNotNone(snippet.id, "Can't create a snippet with serializer")
            return

        self.assertFalse(True, "Can't validate data in snippet serializer for updating")


   