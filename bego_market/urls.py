from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import home, about, payment_and_delivery, laboratory, contact
# from store.views import filter_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('payment_and_delivery/', payment_and_delivery, name='payment_and_delivery'),
    path('laboratory/', laboratory, name='laboratory'),
    path('contact/', contact, name='contact'),
    path('store/', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('account/', include('accounts.urls')),
    # path('filter-data/', filter_data, name='filter_data'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
