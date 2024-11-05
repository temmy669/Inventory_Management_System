from django.db import models
from products.models import Product

class Inventory(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.productID.name} - Quantity: {self.quantity}"
    
# Model to keep a historical record of the Inventory reports generated
class InventoryReport(models.Model):
    report_data = models.JSONField()
    generated_at = models.DateTimeField(auto_now_add=True)

# Model to keep a historical record of the supplier performance reports generated
class SupplierPerformanceReport(models.Model):
    report_data = models.JSONField()
    generated_at = models.DateTimeField(auto_now_add=True)

#Model to store notification status and their status
class Notification(models.Model):
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # Track if the notification has been read
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification: {self.message[:20]}"

