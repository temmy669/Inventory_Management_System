from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Supplier

class SupplierAPITestCase(APITestCase):
    def setUp(self):
        """Set up initial data for testing."""
        self.supplier = Supplier.objects.create(name='Test Supplier', contact_info='contact@test.com')

    def test_list_suppliers(self):
        """Test listing all suppliers."""
        url = reverse('supplier-list')  # Ensure this corresponds to your route
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if we get one supplier in response

    def test_add_supplier(self):
        """Test adding a new supplier."""
        url = reverse('supplier-list')  # Ensure this corresponds to your route
        data = {
            "name": "New Supplier",
            "contact_info": "newsupplier@test.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the supplier was added
        self.assertEqual(Supplier.objects.count(), 2)  # Check if count is now 2
        self.assertEqual(Supplier.objects.get(id=response.data['id']).name, "New Supplier")

    def test_update_supplier(self):
        """Test updating supplier details."""
        url = reverse('supplier-detail', args=[self.supplier.id])  # Ensure this corresponds to your route
        data = {
            "name": "Updated Supplier",
            "contact_info": "updatedsupplier@test.com"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the supplier details were updated
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, "Updated Supplier")
        self.assertEqual(self.supplier.contact_info, "updatedsupplier@test.com")

    def test_delete_supplier(self):
        """Test removing a supplier."""
        url = reverse('supplier-detail', args=[self.supplier.id])  # Ensure this corresponds to your route
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify that the supplier was deleted
        self.assertEqual(Supplier.objects.count(), 0)  # Check if count is now 0
