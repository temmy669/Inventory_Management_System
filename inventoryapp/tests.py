from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Product
from suppliers.models import Supplier
from inventoryapp.models import Inventory

class InventoryViewSetTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Setting up test data for all test methods
        cls.supplier = Supplier.objects.create(name="Test Supplier", contact_info="Contact Info")
        cls.product = Product.objects.create(name="Test Product", description="Test Description", price=10.0, supplier=cls.supplier)
        cls.inventory = Inventory.objects.create(productID=cls.product, quantity=50)

    def test_inventory_list(self):
        # Test GET request to retrieve inventory list
        url = reverse('inventory-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        print(response.data)  # For debugging purposes, can be removed later

    def test_inventory_update(self):
        # Test PATCH request to update inventory quantity
        url = reverse('inventory-detail', args=[self.inventory.id])  # Use 'inventory-detail' for updating a specific instance
        response = self.client.patch(url, {"quantity": 60}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 60)

    def test_generate_inventory_report(self):
        # Test action to generate inventory report
        url = reverse('inventory-generate-inventory-report')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "Inventory Report generation initiated!")

    def test_generate_supplier_report(self):
        # Test action to generate supplier performance report
        url = reverse('inventory-generate-supplier-report')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "Supplier Report generation initiated!")

