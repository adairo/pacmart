from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Producto, Valoracion,Carrito,Producto_carrito
from .forms import ValForm
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.contrib import messages



class Tienda_vista(ListView):
    model = Producto
    template_name = 'store/tienda.html'

class Producto_vista(DetailView):
    model = Producto
    context_object_name = 'producto'
    template_name = 'store/producto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['valoracion_id'] = self.evaluado()
        return context

    def evaluado(self):
        #las siguientes dos líneas me llevaron horas de documentación ._.
        producto = self.get_object()
        user_id = self.request.user
        try:
            val_id = Valoracion.objects.get(producto=producto, autor=user_id).pk
        except Valoracion.DoesNotExist:
            val_id = False
        return val_id
        

@login_required()
def carrito(request):
    
    usrLogueado = User.objects.filter(username = request.user)
    elCarrito = Carrito.objects.filter(user = usrLogueado[0].id,finalizado = False).first()

    productosEnCarrito = Producto_carrito.objects.filter(carrito = elCarrito)
    total = 0
    for item in productosEnCarrito:
        total = total + (item.cantidad * item.producto.precio)
    context = {"carrito":elCarrito,"items":productosEnCarrito,"total":total}     
    return render(request, 'store/carrito.html', context)

def pago(request):
    usrLogueado = User.objects.filter(username = request.user)
    elCarrito = Carrito.objects.filter(user = usrLogueado[0].id,finalizado = False).first()

    productosEnCarrito = Producto_carrito.objects.filter(carrito = elCarrito)
    total = 0
    for item in productosEnCarrito:
        total = total + (item.cantidad * item.producto.precio)
    context = {"carrito":elCarrito,"items":productosEnCarrito,"total":total}     
    
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


class Valorar(View):
    
    form_class = ValForm
    template_name = 'store/valorar_prod.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        producto = get_object_or_404(Producto, pk=kwargs['producto_id'])
        return render(request, self.template_name, {'form': form, 'producto':producto})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        producto = get_object_or_404(Producto, pk=kwargs['producto_id'])
        if form.is_valid():
            val = form.save(commit=False)
            val.producto = producto
            val.autor = request.user
            val.fecha_cre = timezone.now()
            val.save()
            return redirect('store:producto', slug=producto.slug)

        return render(request, self.template_name, {'form': form})


class Editar_Valoracion(View):
    
    form_class = ValForm
    template_name = 'store/valorar_prod.html'

    def get(self, request, *args, **kwargs):
        val = get_object_or_404(Valoracion, pk = kwargs['valoracion_id'])
        form = ValForm(instance=val)
        producto = get_object_or_404(Producto, pk=val.producto.pk)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        val = get_object_or_404(Valoracion, pk = kwargs['valoracion_id'])
        form = self.form_class(request.POST, instance=val)
        producto = get_object_or_404(Producto, pk=val.producto.pk)
        if form.is_valid():
            val = form.save(commit=False)
            val.producto = producto
            val.autor = request.user
            val.fecha_cre = timezone.now()
            val.save()
            return redirect('store:producto', slug=producto.slug)

        return render(request, self.template_name, {'form': form})

