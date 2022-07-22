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
    path('lend/',lend,name='lend'),
    path('activity/',activity,name='activity'),
    path('product/borrow/<int:idn>',borrow,name='borrow'),
    path('accept/<int:idn>',accept,name='acceptreq'),
    path('decline/<int:idn>',decline,name='declinereq'),
    path('filterit/',filterit,name='filterit'),
    path('prodreceived/<int:idn>',prodreceived,name='prodreceived'),
    path('reportuser/<int:idn>', reportuser, name='reportuser'),
    path('reportcomment/', reportcomment, name='reportcomment'),
    path('reportsuccess/', reportsuccess, name='reportsuccess'),
    path('wishlist/', wishlist, name='wishlist'),
    path('profile/', profile, name='profile'),
    path('profileedit/', profileedit, name='profileedit'),
    path('rateborrower/', rateborrower, name='rateborrower'),
    path('ratelender/', ratelender, name='ratelender'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)