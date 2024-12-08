from django.test import TestCase
from .factories import PublicationFactory, CommentFactory, CustomUserFactory

class CommentTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory()
        self.publication = PublicationFactory()
        self.comment = CommentFactory(publication=self.publication, author=self.user)

    def test_comment_data(self):
        self.assertTrue(self.comment.content)
        self.assertEqual(self.comment.publication, self.publication)
        self.assertEqual(self.comment.author, self.user)