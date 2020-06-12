from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .models import Producto


class Tienda_vista(ListView):
    model = Producto
    template_name = 'store/tienda.html'

class Producto_vista(DetailView):
    model = Producto
    template_name = 'store/producto.html'

def carrito(request):
    context = {}
    return render(request, 'store/carrito.html', context)

def pago(request):
    context = {}
    return render(request, 'store/pago.html', context)

def iniciar_sesion(request):
    context = {'titulo':'Iniciar sesión'}
    return render(request, 'store/iniciar_sesion.html', context)

def crear_cuenta(request):
    context = {'titulo':'Crear cuenta'}
    return render(request, 'store/crear_cuenta.html', context)

def pedidos(request):
    context = {'titulo':'Mis pedidos'}
    return render(request, 'store/pedidos.html', context)



# Create your views here.
