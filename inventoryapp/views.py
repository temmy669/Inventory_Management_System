from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import InventorySerializer
from .models import Inventory
from inventoryapp.tasks import generate_inventory_report, generate_supplier_performance_report
from rest_framework.decorators import action

class InventoryViewSet(viewsets.ModelViewSet):

    #define the 
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    @action(detail=False, methods=['post'], url_path='generate-supplier-report')
    def generate_supplier_report(self, request):
        # Queue the task
        generate_supplier_performance_report.delay()  
        return Response({"status": "Supplier Report generation initiated!"})

    @action(detail=False, methods=['post'], url_path='generate-inventory-report')
    def generate_inventory_report(self, request):
        # Queue the task
        generate_inventory_report.delay()
        return Response({"status": "Inventory Report generation initiated!"})