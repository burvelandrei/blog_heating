from django.test import TestCase
from .models import Tag
from .factories import TagFactory

class CategoryTestCase(TestCase):
    def test_create_category(self):
        tag = TagFactory()
        self.assertIsInstance(tag, Tag)
        self.assertIsNotNone(tag.name)
        self.assertIsNotNone(tag.description)