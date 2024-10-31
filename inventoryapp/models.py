from django.db import models
from products.models import Product

class Inventory(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_levels')
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"
    
# Model to keep a historical record of the Inventory reports generated
class InventoryReport(models.Model):
    report_data = models.JSONField()
    generated_at = models.DateTimeField(auto_now_add=True)

# Model to keep a historical record of the supplier performance reports generated
class SupplierPerformanceReport(models.Model):
    report_data = models.JSONField()
    generated_at = models.DateTimeField(auto_now_add=True)

