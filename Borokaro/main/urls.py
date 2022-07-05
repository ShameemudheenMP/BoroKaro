from django.urls import path
from .views import log_in, sign_up, home


urlpatterns = [
    path('home/', home, name='home'),
    # path('home/', home, name='home'),
    path('signup/', sign_up, name='signup'),
    path('login/', log_in, name='login')
]