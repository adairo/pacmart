from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import url
from . import views


app_name='store'
urlpatterns = [
    path('', views.Listar_Productos.as_view(), name='tienda'),
    path('producto/<slug>/', views.Ver_Producto.as_view(), name='producto'),
    path('carrito/', views.carrito, name='carrito'),
    path('pago/', views.pago, name='pago'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar-sesion'),
    path('crear_cuenta/', views.crear_cuenta, name='crear-cuenta'),
    path('pedidos/', views.Ver_pedidos.as_view(), name='pedidos'),
    path('valorar/<int:producto_id>/', views.Valorar_Producto.as_view(), name='new-valorar'),
    path('editar/valoracion/<int:valoracion_id>', views.Editar_Valoracion.as_view(), name='edit-valorar'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)