from celery import shared_task
from inventoryapp.models import Inventory, InventoryReport, SupplierPerformanceReport, Notification
from suppliers.models import Supplier
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
import json

@shared_task
def generate_inventory_report():
    low_stock_threshold = 40  # low stock threshold
    
    #Filter current stock amount with low stock threshold
    low_stock_inventory = Inventory.objects.filter(quantity__lt=low_stock_threshold) 

    # Convert QuerySet to a list of dictionaries
    low_stock_products = list(low_stock_inventory.values('productID__name', 'quantity'))

    report = {
        'low_stock_products': low_stock_products,
        'timestamp': timezone.now().isoformat()
    }

    #convert report to json string
    report__json = json.dumps(report)

    #Save the report to the database
    InventoryReport.objects.create(report_data=report__json)

    

    if low_stock_products:
        for product in low_stock_products:
            # Create a notification without a user association
           notification =  Notification.objects.create(
                message=f"{product['productID__name']} is running low on stock (Quantity: {product['quantity']})."
            )  
        print(notification.message)
    
    return report

@shared_task
def generate_supplier_performance_report():
    suppliers = Supplier.objects.all()
    performance_data = []

    for supplier in suppliers:
        total_products = supplier.products.count()

        #define total_sales while converting product' price to float which is a json serializable format that can be stored in the database
        total_sales = sum(float(product.price) for product in supplier.products.all())  # This assumes price reflects sales
        performance_data.append({
            'supplier_name': supplier.name,
            'total_products': total_products,
            'total_sales': total_sales,
        })
    
    report = {
        'timestamp': timezone.now().isoformat(),
        'supplier_performance': performance_data
    }

    #convert report to a JSON string
    report__json = json.dumps(report)

    # Save the report to the database
    SupplierPerformanceReport.objects.create(report_data=report__json)

    return report
