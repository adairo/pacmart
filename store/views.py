from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Producto, Valoracion, Carrito, Producto_carrito, Producto_comprado,Direccion
from .forms import ValForm
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.contrib import messages


class Listar_Productos(ListView):
    template_name = 'store/tienda.html'
    origen = "Últimos productos agregados"
    queryset = Producto.objects.order_by('-fecha_cre')

    def get(self, request, *args, **kwargs):
        terminos = request.GET.get('terminos')

        if self.queryset:
            if terminos != '' and terminos is not None:
               self.buscar_producto(terminos)
        else:
            self.origen = "Aún no hay productos registrados"

        context = {'origen':self.origen, 'queryset':self.queryset}
        return render(request, self.template_name, context)


    def buscar_producto(self, terminos):
        resultados = self.queryset.filter(
                        titulo__icontains=terminos)
        if resultados is not None:     
            self.origen = f'Se muestran ({len(resultados)}) resultados para "{terminos}"'
            self.queryset = resultados
        else:
            self.origen = f'No se encontraron coincidencias para ("{terminos})"'

    
class Ver_Producto(DetailView):
    model = Producto
    context_object_name = 'producto'
    template_name = 'store/producto.html'
    producto_comprado = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        promedio = self.get_object().get_promedio()
        if self.verificar_compra():
            self.producto_comprado = True
            context['valoracion_id'] = self.evaluado()
        context['comprado'] = self.producto_comprado
        context['promedio']=promedio
        context['positiva']=range(1,int(promedio)+1)
        context['negativa']=range(1,5-int(promedio)+1)
        return context

    def evaluado(self):
        '''Determina si el usuario ya ha escrito una valoración 
        para el producto en cuestion'''

        producto = self.get_object()
        user_id = self.request.user
        try:
            val_id = Valoracion.objects.get(producto=producto, 
                autor=user_id).pk

        except (Valoracion.DoesNotExist, TypeError):
            return False
        return val_id

    def verificar_compra(self):
        '''Determina si un producto ha sido comprado por el usuario que está visitando
        la página de ese producto '''

        usuario = self.request.user
        producto = self.get_object()
        comprado = False
        prod_comprados = usuario.comprados.all()
       
        for prod_c in prod_comprados:
            if prod_c.producto.pk == producto.pk:
                comprado = True

        return comprado


@login_required()
def carrito(request):
    metodo = "GET"
    # aqui traemos al usuario que esta logueado en la request 
    ArregloUsrLogueado = User.objects.filter(username = request.user)
    usrLogueado = ArregloUsrLogueado[0]
    # aqui traemos el carrito asociado a ese usuario logueado
    elCarrito = Carrito.objects.filter(user = usrLogueado.id,finalizado = False).first()
    if not elCarrito:
        elCarrito = Carrito.objects.create(user= usrLogueado)

    if request.method == "POST":
        metodo = "POST con id = "+ request.POST["idProducto"] + ", y cantidad = "+ request.POST["cantidad"]

        productoExistenteEnCarrito = Producto_carrito.objects.filter(carrito = elCarrito, producto = request.POST["idProducto"])
        if productoExistenteEnCarrito:
            # Aqui debemos incrementar ese itemn en tantos como tenga cantidad 
            productoCarritoAActualizar = productoExistenteEnCarrito.first()
            productoCarritoAActualizar.cantidad = productoCarritoAActualizar.cantidad + int(request.POST["cantidad"])
            if productoCarritoAActualizar.cantidad < 1:
                productoCarritoAActualizar.delete()
            else:
                productoCarritoAActualizar.save()
        else:
            # se crea un nuevo producto carrito con ese id de producto
            elProducto = Producto.objects.get(id = request.POST["idProducto"])
            nuevoProductoCarrito = Producto_carrito.objects.create(user = usrLogueado, producto = elProducto,carrito = elCarrito,cantidad = int(request.POST["cantidad"]))

    productosEnCarrito = Producto_carrito.objects.filter(carrito = elCarrito)
    total = 0
    for item in productosEnCarrito:
        total = total + (item.cantidad * item.producto.precio)
    context = {"carrito":elCarrito,"items":productosEnCarrito,"total":total,"metodo":metodo}     
    return render(request, 'store/carrito.html', context)


def pago(request):
    usrLogueado = User.objects.filter(username = request.user)
    elCarrito = Carrito.objects.filter(user = usrLogueado[0].id,finalizado = False).first()
    currentDirSelected = None
    compraTerminada = False
    productosEnCarrito = Producto_carrito.objects.filter(carrito = elCarrito)
    total = 0
    for item in productosEnCarrito:
        total = total + (item.cantidad * item.producto.precio)
    post = request.POST
    if request.method == "POST":
        if not post.get("idDireccion") is None:
            print ("Entro a id direccion")
            currentDirSelected = Direccion.objects.get(id =post["idDireccion"])
            elCarrito.dir_entrega = currentDirSelected
            elCarrito.save()
        elif not post.get("idCarrito") is None:
            print ("Entro a id carrito")
            elCarrito.finalizado = True
            elCarrito.fecha_fin = timezone.now()
            elCarrito.save()
            compraTerminada = True
            agregar_a_comprados(request, productosEnCarrito)

        else:
            print ("Entro a crear direccion")

            Direccion.objects.create(user = usrLogueado.first(),nombre = post["name"],
                                         calle = post["address"], numero= post["number"],
                                         colonia= post["colonia"],cod_postal= post["zipcode"] )
            

    misDirecciones = Direccion.objects.filter(user=usrLogueado.first())

    context = {"compraTerminada":compraTerminada,"carrito":elCarrito,"items":productosEnCarrito,
                                                        "total":total,"misDirecciones":misDirecciones,
                                                        "currentDirSelected":currentDirSelected}     
    return render(request, 'store/pago.html', context)


def agregar_a_comprados(request, productos):
    '''Para cada compra realizada por un cliente, este método recibe un queryset
    que contiene  los productos del carrito que fue finalizado'''

    #la forma de obtener referencias de usuario y producto además de ciertos aspectos
    # de este método pueden variar según el lugar donde sean usadas, esto es una guía

    usuario = request.user

    #el campo 'comprados' hace referencia al parámetro 'related_names' en el atributo user 
    #de la clase Producto_comprado
    prod_comprados = usuario.comprados.all()
 
    for producto_del_carrito in productos:
        if producto_del_carrito.producto not in prod_comprados:
            nuevo_comprado = Producto_comprado(user=usuario,
                             producto=producto_del_carrito.producto)
            nuevo_comprado.save()
    

def iniciar_sesion(request):
    context = {'titulo':'Iniciar sesión'}
    return render(request, 'store/iniciar_sesion.html', context)


def crear_cuenta(request):
    context = {'titulo':'Crear cuenta'}
    return render(request, 'store/crear_cuenta.html', context)


class Ver_pedidos(View):
    template_name = 'store/pedidos.html'

    def get(self,request,*args, **kwargs):
        user = request.user
        carritos = user.carritos.all()
        carritos = carritos.filter(finalizado = True)
        context = {'titulo':'Pedidos', 'pedidos':carritos}
        return render(request, self.template_name, context)
        


class Valorar_Producto(View):
    
    form_class = ValForm
    template_name = 'store/valorar_prod.html'
    

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        producto = get_object_or_404(Producto, pk=kwargs['producto_id'])
        context = {'form':form, 'producto':producto}
        return render(request, self.template_name, context)

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

