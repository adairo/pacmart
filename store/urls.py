from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import url
from . import views


app_name='store'
urlpatterns = [
    path('', views.Tienda_vista.as_view(), name='tienda'),
    path('producto/<slug>/', views.Producto_vista.as_view(), name='producto'),
    path('carrito/', views.carrito, name='carrito'),
    path('pago/', views.pago, name='pago'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar-sesion'),
    path('crear_cuenta/', views.crear_cuenta, name='crear-cuenta'),
    path('pedidos/', views.pedidos, name='pedidos'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)