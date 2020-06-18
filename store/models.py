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
#
#   IMPORTANTE: solo es necesario hacer migraciones cuando se modifican los atributos
#   de las clases modelo y sus relaciones. Cuando se modifican tuplas como CATEGORIAS, o incluso
#   métodos de las clases modelo como get_absolute_url en Producto, NO es necesario migrar.


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
            ('OT',  'Otros'),
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

    descripcion =   models.TextField(default="Descripción")

    #El campo slug brinda una URL única a cada producto
    #Si este campo se deja vacío ocasiona conflictos incluso en la base de datos. 
    slug        =   models.SlugField(blank=False, null=False)

    #Fecha de creación se agrega automáticamente
    fecha_cre   =   models.DateTimeField(auto_now_add=True)
    #Fecha de modificación se actualiza automáticamente
    fecha_mod   =   models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('store:producto', kwargs={'slug':self.slug})

    def get_short_description(self):
        ''' Regresa una versión reducida de la descripción, para ser 
        mostrada en la pantalla carrito'''
        
        if self.descripcion:
            if len(self.descripcion) > 77:
                return self.descripcion[:74]+"..."
            else:
                return self.descripcion
        else:
            return "Producto sin descripcion..."
    
    def get_precio(self):
        '''Regresa el precio expresado como un entero, 
           siempre y cuando no haya pérdida de info'''

        if self.precio.is_integer():
            return int(self.precio)
        return self.precio
		
    def get_promedio(self):
        pass
        # for comentario in valoracion:
        #     sumas=sumas+item.comentario
        #     suma =suma+choices.puntuacion
        # promedio =suma/sumas
        # return int(self.promedio)
        # return self.promedio


class Producto_comprado(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comprados')
    producto    = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"producto:{self.producto.titulo}, comprado por:{self.user.username}"


class Carrito(models.Model):
    '''La clase Carrito contiene la lista de productos que el cliente ha seleccionado para comprar,
       una instancia de Carrito tiene un estado inicial de finalizado=False, esto significa que
       el pedido no ha sido concretado y el carrito puede editarse. Un pedido finalizado no es más
       que una instancia especial de Carrito.'''

    user        =   models.ForeignKey(User, on_delete=models.CASCADE)
    finalizado  =   models.BooleanField(default=False)
    fecha_crea  =   models.DateTimeField(default=timezone.now)
    fecha_fin   =   models.DateTimeField(null=True)
    dir_entrega =   models.ForeignKey('Direccion', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"carrito de: {self.user.username}"

 
class Producto_carrito(models.Model):
    '''Para poder llevar a cabo un pedido, es necesario agregar artículos al carrito,
       La clase Producto_carrito nos permite representar un producto dentro del carrito
       además de la cantidad asociada a ese producto.'''
    user        =   models.ForeignKey(User, on_delete=models.CASCADE)
    finalizado  =   models.BooleanField(default=False)
    producto    =   models.ForeignKey(Producto, on_delete=models.CASCADE)
    carrito     =   models.ForeignKey(Carrito, on_delete=models.CASCADE)
    cantidad    =   models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.producto.titulo} ({self.cantidad})"


class Direccion(models.Model):
    user        =   models.ForeignKey(User, on_delete=models.CASCADE)
    calle       =   models.CharField(max_length=50)
    numero      =   models.CharField(max_length=50)
    colonia     =   models.CharField(max_length=50)
    cod_postal  =   models.CharField(max_length=20)

    def __str__(self):
        return f"dir de: {self.user.username}"


class Valoracion(models.Model):
    producto    =   models.ForeignKey(Producto, on_delete=models.CASCADE, 
                                                related_name='valoraciones')
    autor       =   models.ForeignKey(User, on_delete=models.CASCADE)
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
