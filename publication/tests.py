from django.test import TestCase, Client
from django.urls import reverse
from .models import Publication, Article, Video
from category.models import Category
from comment.models import Comment
from .factories import ArticleFactory, VideoFactory, PublicationFactory
from category.factories import CategoryFactory
from user.factories import CustomUserFactory
from comment.forms import CommentForm

class ArticleModelTest(TestCase):
    def test_article_creation(self):
        article = ArticleFactory()
        self.assertIsInstance(article, Article)
        self.assertEqual(article.__str__(), article.title)

class VideoModelTest(TestCase):
    def test_video_creation(self):
        video = VideoFactory()
        self.assertIsInstance(video, Video)
        self.assertEqual(video.__str__(), video.title)

class PublicationModelTest(TestCase):
    def test_publication_creation(self):
        publication = PublicationFactory()
        self.assertIsInstance(publication, Publication)
        self.assertEqual(publication.__str__(), publication.title)

    def test_publication_title_auto_fill(self):
        article = ArticleFactory()
        publication = PublicationFactory(content_object=article)
        self.assertEqual(publication.title, article.title)

    def test_publication_with_video(self):
        video = VideoFactory()
        publication = PublicationFactory(content_object=video)
        self.assertEqual(publication.title, video.title)


class PublicationListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')
        self.category = CategoryFactory()
        self.article = ArticleFactory(category=self.category)
        self.video = VideoFactory(category=self.category)
        self.publication_article = PublicationFactory(content_object=self.article)
        self.publication_video = PublicationFactory(content_object=self.video)

    def test_publication_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publication/index.html')
        self.assertIn('publications', response.context)
        self.assertIn(self.publication_article, response.context['publications'])
        self.assertIn(self.publication_video, response.context['publications'])

    def test_publication_list_view_with_category_filter(self):
        response = self.client.get(self.url, {'category': self.category.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.publication_article, response.context['publications'])
        self.assertIn(self.publication_video, response.context['publications'])

    def test_publication_list_view_ordering(self):
        response = self.client.get(self.url, {'sort': 'title'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['publications'].ordered, True)

class PublicationDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUserFactory()
        self.category = CategoryFactory()
        self.article = ArticleFactory(category=self.category)
        self.publication = PublicationFactory(content_object=self.article)
        self.url = reverse('publication_detail', args=[self.publication.id])

    def test_publication_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publication/publication_detail.html')
        self.assertIn('publication', response.context)
        self.assertEqual(response.context['publication'], self.publication)

    def test_publication_detail_view_comments(self):
        comment = Comment.objects.create(publication=self.publication, author=self.user, content="Test comment")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('comments', response.context)
        self.assertIn(comment, response.context['comments'])

    def test_publication_detail_view_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], CommentForm)

    def test_add_comment_via_publication_detail_view(self):
        self.client.force_login(self.user)  
        data = {
            'content': 'Test comment',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.publication, self.publication)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, 'Test comment')