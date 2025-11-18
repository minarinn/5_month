from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreateAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view()),
    
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/<int:id>/', views.ProductRetrieveUpdateDestroyAPIView.as_view()),
    path('products/reviews/', views.ProductWithReviewsListAPIView.as_view()),
    
    path('reviews/', views.ReviewListCreateAPIView.as_view()),
    path('reviews/<int:id>/', views.ReviewRetrieveUpdateDestroyAPIView.as_view()),
]