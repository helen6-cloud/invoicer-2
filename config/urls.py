from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def api_redirect(request):
    return redirect('api/')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.api.urls')),
    path('', api_redirect, name='root_redirect'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)