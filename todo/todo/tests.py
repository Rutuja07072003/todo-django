from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from todo.models import TODOO
from django.utils import timezone

class TodoAppTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user.save()

    # Test the signup view
    def test_signup(self):
        response = self.client.post(reverse('signup'), {
            'fnm': 'Test User',
            'email': 'testuser@example.com',
            'pwd': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Check if it redirects after successful signup
        self.assertTrue(User.objects.filter(username='Test User').exists())

    # Test the login view
    def test_login(self):
        # Login the user created in setUp
        response = self.client.post(reverse('loginn'), {
            'fnm': 'testuser',
            'pwd': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Check if it redirects to the todo page

    # Test the todo view (create a TODO item)
    def test_todo_create(self):
        self.client.login(username='testuser', password='password123')  # Log in
        response = self.client.post(reverse('todo'), {
            'title': 'Test TODO'
        })
        self.assertEqual(response.status_code, 302)  # Check if it redirects after creating a todo item
        self.assertTrue(TODOO.objects.filter(title='Test TODO').exists())

    # Test the todo list view (view all TODO items)
    def test_todo_list(self):
        self.client.login(username='testuser', password='password123')
        # Create a TODO item
        TODOO.objects.create(title="Test Todo 1", user=self.user, date=timezone.now())
        response = self.client.get(reverse('todo'))  # Access the todo page
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Todo 1')  # Check if the item is in the response

    # Test the todo delete view
    def test_todo_delete(self):
        self.client.login(username='testuser', password='password123')
        todo_item = TODOO.objects.create(title="Test Todo to Delete", user=self.user, date=timezone.now())
        response = self.client.get(reverse('delete_todo', args=[todo_item.srno]))  # Access the delete URL
        self.assertEqual(response.status_code, 302)  # Check if it redirects after deletion
        self.assertFalse(TODOO.objects.filter(title="Test Todo to Delete").exists())

    # Test the todo edit view
    def test_todo_edit(self):
        self.client.login(username='testuser', password='password123')
        todo_item = TODOO.objects.create(title="Old Title", user=self.user, date=timezone.now())
        response = self.client.post(reverse('edit_todo', args=[todo_item.srno]), {
            'title': 'New Title'
        })
        self.assertEqual(response.status_code, 302)  # Check if it redirects after editing
        todo_item.refresh_from_db()  # Refresh the object to get the latest data from the database
        self.assertEqual(todo_item.title, 'New Title')

    # Test the signout view
    def test_signout(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 302)  # Check if it redirects after logout
        self.assertFalse('_auth_user_id' in self.client.session)  # Ensure the user is logged out
