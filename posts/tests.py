
from django.test import TestCase
from django.urls import reverse
from .models import Post, Author
from .forms import PostForm


class PostModelTest(TestCase):
    def setUp(self):
        # Create an Author object
        author = Author.objects.create(name='Test Author')
        # Create a Post object for testing
        Post.objects.create(title='Test Post', content='This is a test post.', author=author)

    def test_post_has_title(self):
        # Test that a Post object has the expected title
        post = Post.objects.get(id=1)
        self.assertEqual(post.title, 'Test Post')

    def test_post_has_content(self):
        # Test that a Post object has the expected content
        post = Post.objects.get(id=1)
        self.assertEqual(post.content, 'This is a test post.')

    def test_post_string_representation(self):
        # Test that a Post's string representation is its title
        post = Post.objects.get(id=1)
        self.assertEqual(str(post), 'Test Post')

    def test_author_string_representation(self):
        # Test that an Author's string representation is its name
        author = Author.objects.get(name='Test Author')
        self.assertEqual(str(author), 'Test Author')


class PostViewTest(TestCase):
    def setUp(self):
        # Create an Author object
        author = Author.objects.create(name='Test Author')
        # Create a Post object for testing views
        Post.objects.create(title='Test Post', content='This is a test post.', author=author)

    def test_post_list_view(self):
        # Test the post-list view
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        # Test the post-detail view
        post = Post.objects.get(id=1)
        response = self.client.get(reverse('post_detail', args=[str(post.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'This is a test post.')

    def test_post_detail_view_404_for_missing_post(self):
        # Test that a non-existent post returns a 404
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_post_create_view_get(self):
        # Test that the create form renders on GET
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_post_create_view_post(self):
        # Test that a valid POST creates a new post and redirects
        author = Author.objects.get(name='Test Author')
        response = self.client.post(reverse('post_create'), {
            'title': 'New Post',
            'content': 'New post content.',
            'author': author.id,
        })
        self.assertRedirects(response, reverse('post_list'))
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_post_update_view(self):
        # Test that a valid POST updates an existing post and redirects
        post = Post.objects.get(id=1)
        author = Author.objects.get(name='Test Author')
        response = self.client.post(reverse('post_update', args=[post.id]), {
            'title': 'Updated Post',
            'content': 'Updated content.',
            'author': author.id,
        })
        self.assertRedirects(response, reverse('post_list'))
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Post')
        self.assertEqual(post.content, 'Updated content.')

    def test_post_delete_view_get_shows_confirmation(self):
        # Test that GET on delete shows a confirmation page without deleting
        post = Post.objects.get(id=1)
        response = self.client.get(reverse('post_delete', args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(id=post.id).exists())

    def test_post_delete_view_post(self):
        # Test that POST on delete removes the post and redirects
        post = Post.objects.get(id=1)
        response = self.client.post(reverse('post_delete', args=[post.id]))
        self.assertRedirects(response, reverse('post_list'))
        self.assertFalse(Post.objects.filter(id=post.id).exists())


class PostFormTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')

    def test_form_valid_with_all_fields(self):
        form = PostForm(data={
            'title': 'Form Post',
            'content': 'Form content.',
            'author': self.author.id,
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_title(self):
        form = PostForm(data={
            'title': '',
            'content': 'Form content.',
            'author': self.author.id,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
