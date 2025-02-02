from django.test import SimpleTestCase
from django.urls import reverse, resolve
from loadns import views

class TestUrls(SimpleTestCase):

    def test_loan_index_url_resolves(self):
        url = reverse('loan.index')
        self.assertEqual(resolve(url).func, views.loan_main)

    def test_loan_create_url_resolves(self):
        url = reverse('loan.create')
        self.assertEqual(resolve(url).func, views.loan_create)

    def test_loan_show_url_resolves(self):
        url = reverse('loan.show', args=[1])
        self.assertEqual(resolve(url).func, views.loan_show)

    def test_loan_update_url_resolves(self):
        url = reverse('loan.update', args=[1])
        self.assertEqual(resolve(url).func, views.loan_update)

    def test_loan_delete_url_resolves(self):
        url = reverse('loan.delete', args=[1])
        self.assertEqual(resolve(url).func, views.loan_delete)

    def test_loan_return_url_resolves(self):
        url = reverse('loan.return', args=[1])
        self.assertEqual(resolve(url).func, views.loan_return)