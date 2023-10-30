from django.urls import path
from django.urls import include
from django.contrib import admin
from Site.views import index
from django.conf.urls.static import static
from Site.settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    path('restorations/',        include('Restorations.urls')),
    path('restorations_api/v1/', include('Restorations.api_v1.urls')),
    path('profiles_api/v1/',     include('Profiles.api_v1.urls')),
    path('admin/', admin.site.urls),
    path('', index)
]

# Should be changed on production:
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
