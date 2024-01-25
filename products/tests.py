from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from products.models import Product, ProductsCategoty
# Create your tests here.

class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Welcome!!!')
        self.assertTemplateUsed(response, 'products/index.html')

class ProductsViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def test_list(self):
        products = Product.objects.all()
        path = reverse('products:index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(list(response.context_data['object_list']), list(products[:3]))

    def test_category_product(self):
        category = ProductsCategoty.objects.first()

        products = Product.objects.filter(category_id = category.id)
        path = reverse('products:category', kwargs={'category_id' : category.id})
        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(list(response.context_data['object_list']), list(products[:3]))
    
