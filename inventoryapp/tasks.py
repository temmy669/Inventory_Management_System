from celery import shared_task
from inventoryapp.models import Inventory, InventoryReport, SupplierPerformanceReport 
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
    low_stock_products = list(low_stock_inventory.values('product__name', 'quantity'))

    report = {
        'low_stock_products': low_stock_products,
        'timestamp': timezone.now().isoformat()
    }

    #Save the report to the database
    InventoryReport.objects.create(report_data=report)

    # Trigger an email alert if there are low-stock products

    if low_stock_products:  # Check if the list is not empty
        send_mail(
            subject='Low Stock Alert',
            message='Some products are running low on stock.',
            from_email=settings.LOW_STOCK_ALERT_EMAIL,
            recipient_list=settings.INVENTORY_MANAGER_EMAILS,
        )

    
    
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