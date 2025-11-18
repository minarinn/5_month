from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    CategoryValidateSerializer,
    ProductSerializer,
    ProductValidateSerializer,
    ReviewSerializer,
    ReviewValidateSerializer,
    ProductWithReviewsSerializer
)
from .pagination import CustomPagination

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination
    
    def post(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        
        category = Category.objects.create(
            name=validated_data['name']
        )
        
        return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)

class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        
        instance.name = validated_data['name']
        instance.save()
        
        return Response(CategorySerializer(instance).data, status=status.HTTP_201_CREATED)

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    
    def post(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        
        product = Product.objects.create(
            title=validated_data['title'],
            description=validated_data.get('description', ''),
            price=validated_data['price'],
            category_id=validated_data['category_id']
        )
        
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        
        instance.title = validated_data['title']
        instance.description = validated_data.get('description', '')
        instance.price = validated_data['price']
        instance.category_id = validated_data['category_id']
        instance.save()
        
        return Response(ProductSerializer(instance).data, status=status.HTTP_201_CREATED)

class ProductWithReviewsListAPIView(generics.ListAPIView):
    queryset = Product.objects.all().prefetch_related('reviews')
    serializer_class = ProductWithReviewsSerializer
    pagination_class = CustomPagination

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination
    
    def post(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        
        review = Review.objects.create(
            text=validated_data['text'],
            product_id=validated_data['product_id'],
            stars=validated_data['stars']
        )
        
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        
        instance.text = validated_data['text']
        instance.product_id = validated_data['product_id']
        instance.stars = validated_data['stars']
        instance.save()
        
        return Response(ReviewSerializer(instance).data, status=status.HTTP_201_CREATED)