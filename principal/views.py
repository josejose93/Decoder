# Create your views here.
from principal.models import Decodificador
from principal.forms import AgregarArchivosForm, DecodificarForm, BuscarForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from principal.processor import Decoder, Encoder
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from principal.interpreter import OrExpression

def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/privado')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid():
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/privado')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html', context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('index.html', {'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def privado(request):
	usuario = request.user
	return render_to_response('inicio.html', {'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/ingresar')
#    return render_to_response('subir_archivos.html', {'form': form}, context_instance=RequestContext(request))

def nuevo_archivo(request):
	if request.user.is_authenticated():
		if request.method=='POST':
			formulario = AgregarArchivosForm(request.POST, request.FILES)
			if formulario.is_valid():
				titulo = formulario.cleaned_data['titulo']
				imagen = formulario.cleaned_data['imagen']
				archivo = formulario.cleaned_data['archivo']
				imgpath = default_storage.save('tmp/'+imagen._get_name(), ContentFile(imagen.read()))
				archpath = default_storage.save('tmp/'+archivo._get_name(), ContentFile(archivo.read()))
				encode = Encoder()
				img = encode(str(default_storage.path(imgpath)), str(default_storage.path(archpath)))
				savepath = str(default_storage.path('imagenes/' + titulo))
				img.save(savepath)
				default_storage.delete(imgpath)
				default_storage.delete(archpath)
				nuevo = Decodificador(usuario = request.user, titulo = titulo, imagen = 'imagenes/' + titulo +'.png')
				nuevo.save()
				return HttpResponseRedirect('/inicio') 
		else:
			formulario = AgregarArchivosForm()
		return render_to_response('subir_archivos.html', {'formulario':formulario}, context_instance=RequestContext(request))

def recuperar_archivo(request):
	if request.user.is_authenticated():
		if request.method=='POST':
			formulario = DecodificarForm(request.POST, request.FILES)
			if formulario.is_valid():
				imagen = formulario.cleaned_data['imagen']
				imgpath = default_storage.save('tmp/'+imagen._get_name(), ContentFile(imagen.read()))
				decode = Decoder()
				savepath = default_storage.path('tmp/decoded')
				archivo = decode(str(default_storage.path(imgpath)), str(savepath))
				default_storage.delete(imgpath)
				size = archivo.size()
				extension = archivo.get_extension()
				savepath += '.' + extension
				archivo = default_storage.open(savepath)
				data = archivo.read()
				archivo.close()
				response = HttpResponse(data, content_type='aplication/octet-stream')
				response['Content-Length']= size
				response['Content-Disposition'] = 'attachment; filename="descarga.'+extension+'"'
				default_storage.delete(savepath)
				return response 
		else:
			formulario = DecodificarForm()
		return render_to_response('decodificar_foto.html', {'formulario':formulario}, context_instance=RequestContext(request))
	

def inicio(request):
	if request.user.is_authenticated():
		usuario = request.user
		ini = Decodificador.objects.all()
		return render_to_response('inicio.html', {'deco':ini, 'usuario':usuario}, context_instance=RequestContext(request))
	else:
		return render_to_response('busqueda.html', {'formulario': BuscarForm()}, context_instance=RequestContext(request))

def buscar(request):
    formulario = BuscarForm(request.GET)
    if formulario.is_valid():
        query = formulario.cleaned_data['query']
        resultados = Decodificador.objects.filter(OrExpression().interpret(query))
        print(query)
	return render_to_response('busqueda.html', {'formulario': formulario, 'resultados': resultados}, context_instance=RequestContext(request))

#def handle_uploaded_file(f, instance):
#    instance.field.save('name_slug.ext', f, True)
#    instance.save()
