from django.urls import path
from .views import log_in, sign_up, home, product


urlpatterns = [
    path('home/', home, name='home'),
    path('', home, name='home'),
    path('signup/', sign_up, name='signup'),
    path('login/', log_in, name='login'),
    path('product/',product,name='product') #ADDED PRODUCT PAGE JUST FOR PRESENTATION
]