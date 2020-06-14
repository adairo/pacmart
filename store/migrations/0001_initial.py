# Generated by Django 3.0.7 on 2020-06-14 02:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=30)),
                ('precio', models.FloatField(default=0)),
                ('codigo', models.CharField(blank=True, max_length=10)),
                ('imagen', models.ImageField(default='product_thumb_placeholder.png', upload_to='product_thumbs')),
                ('categoria', models.CharField(choices=[('IN', 'Indeterminado'), ('EL', 'Electrónicos'), ('DS', 'Deportes'), ('ED', 'Electrodomésticos'), ('LB', 'Libros'), ('MS', 'Moda/Estilo'), ('AU', 'Audio'), ('VI', 'Video'), ('LB', 'Linea blanca')], default='IN', max_length=10)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField()),
                ('fecha_cre', models.DateTimeField(auto_now=True)),
                ('fecha_mod', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Valoracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.IntegerField(choices=[(1, ' muy malo'), (2, 'malo'), (3, 'regular'), (4, 'bueno'), (5, 'muy bueno')])),
                ('comentario', models.TextField(blank=True, null=True)),
                ('fecha_cre', models.DateField(auto_now_add=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='valoraciones', to='store.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Producto_carrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finalizado', models.BooleanField(default=False)),
                ('cantidad', models.IntegerField(default=1)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Producto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(max_length=50)),
                ('numero', models.CharField(max_length=50)),
                ('colonia', models.CharField(max_length=50)),
                ('cod_postal', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finalizado', models.BooleanField(default=False)),
                ('codigo', models.CharField(blank=True, max_length=20, null=True)),
                ('fecha_crea', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_fin', models.DateTimeField(null=True)),
                ('dir_entrega', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Direccion')),
                ('productos', models.ManyToManyField(to='store.Producto_carrito')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
