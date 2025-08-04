from django.urls import path, include

urlpatterns = [
    path('orders/', include('api.orders.urls')),
    path('products/', include('api.products.urls'))
]
