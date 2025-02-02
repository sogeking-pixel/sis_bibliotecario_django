from django.test import SimpleTestCase
from django.urls import reverse, resolve
from administraction import views


class TestUrls(SimpleTestCase):
    def test_user_index_url_resolves(self):
        url = reverse('user.index')
        self.assertEqual(resolve(url).func, views.user_main)
        
    def test_user_create_url_resolves(self):
        url = reverse('user.create')
        self.assertEqual(resolve(url).func, views.user_create)
        
    def test_user_show_url_resolves(self):
        url = reverse('user.show', args=[1])
        self.assertEqual(resolve(url).func, views.user_show)
        
    def test_user_update_url_resolves(self):
        url = reverse('user.update', args=[1])
        self.assertEqual(resolve(url).func, views.user_update)
        
    def test_user_delete_url_resolves(self):
        url = reverse('user.delete', args=[1])
        self.assertEqual(resolve(url).func, views.user_delete)
        
        

class TestAuthorUrls(SimpleTestCase):
    def test_author_index_url_resolves(self):
        url = reverse('author.index')
        self.assertEqual(resolve(url).func, views.author_main)
        
    def test_author_create_url_resolves(self):
        url = reverse('author.create')
        self.assertEqual(resolve(url).func, views.author_create)
        
    def test_author_show_url_resolves(self):
        url = reverse('author.show', args=[1])
        self.assertEqual(resolve(url).func, views.author_show)
        
    def test_author_update_url_resolves(self):
        url = reverse('author.update', args=[1])
        self.assertEqual(resolve(url).func, views.author_update)
        
    def test_author_delete_url_resolves(self):
        url = reverse('author.delete', args=[1])
        self.assertEqual(resolve(url).func, views.author_delete)



class TestSanctionUrls(SimpleTestCase):
    def test_sanction_index_url_resolves(self):
        url = reverse('sanction.index')
        self.assertEqual(resolve(url).func, views.sanction_main)
        
    def test_sanction_create_url_resolves(self):
        url = reverse('sanction.create')
        self.assertEqual(resolve(url).func, views.sanction_create)
        
    def test_sanction_show_url_resolves(self):
        url = reverse('sanction.show', args=[1])
        self.assertEqual(resolve(url).func,views. sanction_show)
        
    def test_sanction_update_url_resolves(self):
        url = reverse('sanction.update', args=[1])
        self.assertEqual(resolve(url).func, views.sanction_update)
        
    def test_sanction_delete_url_resolves(self):
        url = reverse('sanction.delete', args=[1])
        self.assertEqual(resolve(url).func, views.sanction_delete)