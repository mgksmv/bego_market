from django.urls import path

from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('category/<slug:category_slug>/', views.products, name='products_by_category'),
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('product/filter-product/', views.product_filter, name='product_filter'),
    path('search/', views.search, name='search'),
    path('brands/', views.brands, name='brands'),
    path('brands/<slug:brand_slug>/', views.brand_detail, name='brand_detail'),
]
