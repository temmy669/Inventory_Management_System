from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, Supplier  # Adjust the import based on your project structure

class ProductAPITestCase(APITestCase):
    def setUp(self):
        # Create a test supplier
        self.supplier = Supplier.objects.create(name="Test Supplier", contact_info="Contact Info")

        # Create a test product
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=10.0,
            supplier=self.supplier
        )

    def test_list_products(self):
        """Test retrieving a list of products."""
        url = reverse('product-list')  # Ensure 'product-list' corresponds to your route
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Expect 1 product

    def test_create_product(self):
        """Test creating a new product."""
        url = reverse('product-list')
        data = {
            "name": "New Product",
            "description": "New Product Description",
            "price": 15.0,
            "supplier": self.supplier.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)  # Check that a new product was created

    def test_update_product(self):
        """Test updating an existing product."""
        url = reverse('product-detail', args=[self.product.id])
        data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 12.0,
            "supplier": self.supplier.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()  # Refresh the instance from the database
        self.assertEqual(self.product.name, "Updated Product")

    def test_delete_product(self):
        """Test deleting a product."""
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)  # Check that the product was deleted

