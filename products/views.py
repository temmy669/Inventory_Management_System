from django.shortcuts import render
from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer
from .models import Product
from suppliers.models import Supplier
from rest_framework.decorators import api_view
import pandas as pd
from django.http import JsonResponse

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@api_view(['POST'])
def upload_product_csv(request):
    # Check if a file is provided in the request
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']

    # Check if the uploaded file is a CSV
    if not file.name.endswith('.csv'):
        return JsonResponse({'error': 'File is not a CSV.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file)
        records_processed = 0
        errors = []

        # Check if the required columns exist
        required_columns = ['name', 'description', 'price', 'supplier']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            return JsonResponse({'error': f'Missing columns: {", ".join(missing_columns)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            try:
                # Check if supplier is present in the row
                if pd.isnull(row['supplier']):
                    errors.append({'row': index + 1, 'error': 'Missing supplier'})
                    continue

                # Extract data from the current row
                supplier_name = row['supplier']
                # Get or create a supplier based on the supplier_name
                supplier, created = Supplier.objects.get_or_create(name=supplier_name)

                # Create a new product instance
                product = Product(
                    name=row['name'],
                    description=row['description'],
                    price=row['price'],
                    supplier=supplier
                )
                # Save the product to the database
                product.save()
                records_processed += 1
            except KeyError as e:
                errors.append({'row': index + 1, 'error': f'Missing column: {str(e)}'})
            except Exception as e:
                errors.append({'row': index + 1, 'error': str(e)})

        # Prepare the response data
        response_data = {
            'records_processed': records_processed,
            'total_records': len(df),
            'errors': errors
        }
        return JsonResponse(response_data, status=status.HTTP_201_CREATED)

    except pd.errors.EmptyDataError:
        return JsonResponse({'error': 'The uploaded CSV file is empty.'}, status=status.HTTP_400_BAD_REQUEST)
    except pd.errors.ParserError:
        return JsonResponse({'error': 'The uploaded file is corrupted or not a valid CSV.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'price']  # Fields you want to allow filtering on

    search_fields = ['name', 'description']  # Fields to enable search on

    ordering_fields = ['name', 'price']  # Fields to enable ordering on