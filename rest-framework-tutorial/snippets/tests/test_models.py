from django.test import TestCase
from django.contrib.auth.models import User
from snippets.models import Snippet

class SnippetModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.username = "john"
        cls.email = "john@snow.com"
        cls.password = "secret"

        cls.user = User.objects.create_user(
            cls.username, cls.email, cls.password
        )
        Snippet.objects.create(code='<h2>first snippet</h2>', owner=cls.user)

    def test_title_label(self):
        snippet = Snippet.objects.get(id=1)
        field_label = snippet._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        author = Snippet.objects.get(id=1)
        max_length = Snippet._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

