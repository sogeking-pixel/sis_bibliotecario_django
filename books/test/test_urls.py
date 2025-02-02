from django.test import SimpleTestCase
from django.urls import reverse, resolve
from books import views

class TestBookUrls(SimpleTestCase):
    
    def test_book_index_url_resolves(self):
        url = reverse('book.index')
        self.assertEqual(resolve(url).func, views.book_main)

    def test_book_create_url_resolves(self):
        url = reverse('book.create')
        self.assertEqual(resolve(url).func, views.book_create)

    def test_book_show_url_resolves(self):
        url = reverse('book.show', args=[1])
        self.assertEqual(resolve(url).func, views.book_show)

    def test_book_update_url_resolves(self):
        url = reverse('book.update', args=[1])
        self.assertEqual(resolve(url).func, views.book_update)

    def test_book_delete_url_resolves(self):
        url = reverse('book.delete', args=[1])
        self.assertEqual(resolve(url).func, views.book_delete)



class TestCopyUrls(SimpleTestCase):
    
    def test_copy_index_url_resolves(self):
        url = reverse('copy.index')
        self.assertEqual(resolve(url).func, views.copy_main)

    def test_copy_create_url_resolves(self):
        url = reverse('copy.create')
        self.assertEqual(resolve(url).func, views.copy_create)

    def test_copy_show_url_resolves(self):
        url = reverse('copy.show', args=[1])
        self.assertEqual(resolve(url).func, views.copy_show)

    def test_copy_update_url_resolves(self):
        url = reverse('copy.update', args=[1])
        self.assertEqual(resolve(url).func, views.copy_update)

    def test_copy_delete_url_resolves(self):
        url = reverse('copy.delete', args=[1])
        self.assertEqual(resolve(url).func, views.copy_delete)