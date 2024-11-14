from django.shortcuts import render
from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, ProductUploadSerializer
from .models import Product
from suppliers.models import Supplier
from rest_framework.decorators import api_view
import pandas as pd
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

class upload_product_csv(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ProductUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve the file from the validated data
        file = serializer.validated_data['file']

        # Ensure the file is a CSV
        if not file.name.endswith('.csv'):
            return Response({'error': 'File is not a CSV.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(file, encoding='utf-8')

            records_processed = 0
            errors = []
            required_columns = ['name', 'description', 'price', 'supplier']
            missing_columns = [col for col in required_columns if col not in df.columns]

            # Check if required columns are present
            if missing_columns:
                return Response({'error': f'Missing columns: {", ".join(missing_columns)}'}, status=status.HTTP_400_BAD_REQUEST)

            products_to_create = []
            for index, row in df.iterrows():
                try:
                    if pd.isnull(row['supplier']):
                        errors.append({'row': index + 1, 'error': 'Missing supplier'})
                        continue

                    supplier_name = row['supplier']
                    supplier, created = Supplier.objects.get_or_create(name=supplier_name)

                    product = Product(
                        name=row['name'],
                        description=row['description'],
                        price=row['price'],
                        supplier=supplier
                    )
                    products_to_create.append(product)
                    records_processed += 1
                except KeyError as e:
                    errors.append({'row': index + 1, 'error': f'Missing column: {str(e)}'})
                except IntegrityError as e:
                    errors.append({'row': index + 1, 'error': f'Integrity error: {str(e)}'})
                except Exception as e:
                    errors.append({'row': index + 1, 'error': str(e)})

            # Bulk create all products if there are any valid entries
            if products_to_create:
                Product.objects.bulk_create(products_to_create)

            response_data = {
                'records_processed': records_processed,
                'total_records': len(df),
                'errors': errors
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except pd.errors.EmptyDataError:
            return Response({'error': 'The uploaded CSV file is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        except pd.errors.ParserError:
            return Response({'error': 'The uploaded file is corrupted or not a valid CSV.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    # parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'price']  # Fields you want to allow filtering on

    search_fields = ['name', 'description']  # Fields to enable search on

    ordering_fields = ['name', 'price']  # Fields to enable ordering on