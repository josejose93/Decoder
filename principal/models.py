#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Decodificador(models.Model):
	usuario = models.ForeignKey(User)
	titulo = models.CharField(max_length=100, unique=True)
	imagen = models.ImageField(upload_to='imagenes', verbose_name='Imágen')
	#archivo = models.FileField(upload_to='archivos', verbose_name='Archivos', blank=True)

	def __unicode__(self):
		return self.titulo


