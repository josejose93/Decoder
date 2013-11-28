#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
import os

#class AgregarArchivosForm(ModelForm):
#	class Meta:
#		model = Decodificador


class AgregarArchivosForm(forms.Form):
	titulo = forms.CharField()
	imagen = forms.ImageField()
	archivo = forms.FileField()

class DecodificarForm(forms.Form):
	imagen = forms.ImageField()

class BuscarForm(forms.Form):
	query = forms.CharField(label = "")

#class ModelFormWithFileField(ModelForm):
#	class Meta:
#		model = Decodificador
#		exlude = ('titulo, archivo')
