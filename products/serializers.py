from rest_framework import serializers
from .models import Product
from suppliers.models import Supplier

class ProductSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)  # Read-only field for supplier's name
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), write_only=True)  # Write-only for supplier ID

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'supplier', 'supplier_name']  # Add supplier_id for writes

    def create(self, validated_data):
        supplier = validated_data.pop('supplier')  # Extract supplier_id
        product = Product.objects.create(supplier=supplier, **validated_data)  # Create Product with the supplier
        return product

    def update(self, instance, validated_data):
        if 'supplier' in validated_data:
            supplier = validated_data.pop('supplier')  # Extract supplier_id if provided
            instance.supplier = supplier  # Update supplier reference
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # Update other fields
        instance.save()  # Save the instance
        return instance
