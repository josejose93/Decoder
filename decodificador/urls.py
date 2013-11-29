from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'decodificador.views.home', name='home'),
    # url(r'^decodificador/', include('decodificador.foo.urls')),
    url(r'^$', 'principal.views.inicio'),
    url(r'^inicio/$', 'principal.views.inicio'),
    url(r'^ingresar/$', 'principal.views.ingresar'),
    url(r'^inicio/subir/$', 'principal.views.nuevo_archivo'),
    url(r'^inicio/decodificar/$', 'principal.views.recuperar_archivo'),  
    url(r'^privado/$', 'principal.views.privado'),
    url(r'^cerrar/$', 'principal.views.cerrar'),  
    url(r'^buscar/$', 'principal.views.buscar'),
    url(r'^inicio/galeria/$', 'principal.views.galeria'),
    url(r'^inicio/decogal/(?P<id>\d+)/$', 'principal.views.recuperar_mio'),  
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
)
