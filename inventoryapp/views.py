from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import InventorySerializer, NotificationSerializer
from .models import Inventory, Notification
from inventoryapp.tasks import generate_inventory_report, generate_supplier_performance_report
from rest_framework.decorators import action

class InventoryViewSet(viewsets.ModelViewSet):

    #retrieve all objects from the inventory class 
    queryset = Inventory.objects.all().order_by('id')
  
    serializer_class = InventorySerializer

    @action(detail=False, methods=['get'], url_path='generate-supplier-report')
    def generate_supplier_report(self, request):

        # Queue the task
        report = generate_supplier_performance_report()  
        return Response({"status": "Supplier Report generation initiated!", "report" : report})

    @action(detail=False, methods=['get'], url_path='generate-inventory-report')
    def generate_inventory_report(self, request):
        # Queue the task
        report = generate_inventory_report()
        return Response({"status": "Inventory Report generation initiated!", "report" : report})
    
class NotificationViewSet(viewsets.ViewSet):
    def list(self, request):

        # Query all notifications from the database
        notifications = Notification.objects.all().order_by('-created_at')  # Order by latest
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)