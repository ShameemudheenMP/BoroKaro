from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home/', home, name='home'),
    path('', home, name='home'),
    path('signup/', sign_up, name='signup'),
    path('login/', log_in, name='login'),
    path('product/<int:idn>',product,name='product'),
    path('lend/',lend,name='lend')
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)