from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


urlpatterns = [
    path('favicon.ico',RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),
    path('home/', home, name='home'),
    path('', home, name='home'),
    path('signup/', sign_up, name='signup'),
    path('login/', log_in, name='login'),
    path('product/<int:idn>',product,name='product'),
    path('lend/',lend,name='lend'),
    path('actlend/<int:idn>',actlend,name='actlend'),
    path('activity/',activity,name='activity'),
    path('product/borrow/<int:idn>',borrow,name='borrow'),
    path('accept/<int:idn>',accept,name='acceptreq'),
    path('decline/<int:idn>',decline,name='declinereq'),
    path('filterit/',filterit,name='filterit'),
    path('prodreceived/<int:idn>',prodreceived,name='prodreceived'),
    path('reportuser/<int:idn>', reportuser, name='reportuser'),
    path('repous/<int:idn>', repous, name='repous'),
    path('reportcomment/<int:idn>', reportcomment, name='reportcomment'),
    path('repoco/<int:idn>', repoco, name='repoco'),
    path('reportsuccess/', reportsuccess, name='reportsuccess'),
    path('viewwish',viewwish,name='viewwish'),
    path('wishlist/<int:idn>', wishlist, name='wishlist'),
    path('unwish/<int:idn>', unwish, name='unwish'),
    path('profile/<int:idn>', profile, name='profile'),
    path('profileedit/<int:idn>', profileedit, name='profileedit'),
    path('comment/<int:idn>',comment,name='comment'),
    path('rateborrower/<int:idn>', rateborrower, name='rateborrower'),
    path('ratelender/<int:idn>', ratelender, name='ratelender'),
] 

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)