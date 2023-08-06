from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404

handler404 = 'jobapplication.views.handler_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobapplication.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)