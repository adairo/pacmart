from django.contrib import admin
from .models import (Producto,
                    Producto_carrito,
                    Carrito,
                    Valoracion,
                    Direccion)
                    

admin.site.register(Producto)
admin.site.register(Producto_carrito)
admin.site.register(Carrito)
admin.site.register(Direccion)
admin.site.register(Valoracion)


# Register your models here.
