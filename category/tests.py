from django.test import TestCase
from .models import Category
from .factories import CategoryFactory

class CategoryTestCase(TestCase):
    def test_create_category(self):
        category = CategoryFactory()
        self.assertIsInstance(category, Category)
        self.assertIsNotNone(category.name)
        self.assertIsNotNone(category.description)