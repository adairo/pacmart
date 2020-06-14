from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse

#   Para brindar opciones al atributo 'choices' de models.XField,
#   se pasa una lista que contiene n tuplas que representan las
#   opciones disponibles, cada tupla es un par de
#   (VALOR_REAL, VALOR_LEGIBLE)
#   Un ejemplo de esto son las opciones de categoría en Producto
#   y opciones de puntuacion en Valoracion


#Agreguen cuantas categorías necesiten para hacer pruebas
CATEGORIAS =(
            ('IN',  'Indeterminado'),
            ('EL',  'Electrónicos'),
            ('DS',  'Deportes'),
            ('ED',  'Electrodomésticos'),
            ('LB',  'Libros'),
            ('MS',  'Moda/Estilo'),
            ('AU',  'Audio'),
            ('VI',  'Video'),
            ('LB',  'Linea blanca'),
            ('Ot',  'Otros'),
)

class Producto(models.Model):
    '''La clase Producto contiene los campos necesarios para representar
       un artículo haciendolo único y distinguible de otros productos'''

    titulo      =   models.CharField(max_length=30)
    precio      =   models.FloatField(default=0)
    codigo      =   models.CharField(max_length=10, blank=True)
    imagen      =   models.ImageField(upload_to='product_thumbs', 
                                    default='product_thumb_placeholder.png')

    categoria   =   models.CharField(choices=CATEGORIAS, 
                                    max_length=2, 
                                    default='IN')

    descripcion =   models.TextField(blank=True, null=True)
    slug        =   models.SlugField()  
    #Fecha de creación se agrega automáticamente
    fecha_cre   =   models.DateTimeField(auto_now=True)
    #Fecha de modificación se actualiza automáticamente
    fecha_mod   =   models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('store:producto', kwargs={'slug':self.slug})

 
class Producto_carrito(models.Model):
    '''Para poder llevar a cabo un pedido, es necesario agregar artículos al carrito,
       La clase Producto_carrito nos permite representar un producto dentro del carrito
       además de la cantidad asociada a ese producto.'''
       
    user        =   models.ForeignKey(User, on_delete=models.CASCADE)
    finalizado  =   models.BooleanField(default=False)
    producto    =   models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad    =   models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.producto.titulo} ({self.cantidad})"


class Carrito(models.Model):
    '''La clase Carrito contiene la lista de productos que el cliente ha seleccionado para comprar,
       una instancia de Carrito tiene un estado inicial de finalizado=False, esto significa que
       el pedido no ha sido concretado y el carrito puede editarse. Un pedido finalizado no es más
       que una instancia especial de Carrito.'''

    user        =   models.ForeignKey(User, on_delete=models.CASCADE)
    finalizado  =   models.BooleanField(default=False)
    codigo      =   models.CharField(max_length=20, blank=True, null=True)
    productos   =   models.ManyToManyField(Producto_carrito)
    fecha_crea  =   models.DateTimeField(default=timezone.now)
    fecha_fin   =   models.DateTimeField(null=True)
    dir_entrega =   models.ForeignKey('Direccion', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"carrito de: {self.user.username}"


class Direccion(models.Model):
    user        =   models.ForeignKey(User, on_delete=models.CASCADE)
    calle       =   models.CharField(max_length=50)
    numero      =   models.CharField(max_length=50)
    colonia     =   models.CharField(max_length=50)
    cod_postal  =   models.CharField(max_length=20)

    def __str__(self):
        return f"dir de: {self.user.username}"


class Valoracion(models.Model):
    producto    =   models.ForeignKey(Producto, on_delete=models.CASCADE)
    autor       =   models.OneToOneField(User, on_delete=models.CASCADE)
    puntuacion  =   models.IntegerField(choices=[
                                                (1,' muy malo'), 
                                                (2, 'malo'), 
                                                (3, 'regular'), 
                                                (4, 'bueno'), 
                                                (5, 'muy bueno')])

    comentario  =   models.TextField(blank=True, null=True)

    #   En caso de que prefieras mostrar la hora y fecha en lugar de solo la fecha,
    #   el siguiente atributo debe cambiarse a un modelo de tipo DateTimeField
    fecha_cre   =   models.DateField(auto_now_add=True) 

    def __str__(self):
        return f"de: {self.autor.username}, para:  {self.producto.titulo}"

#Create your models here.
