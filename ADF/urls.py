
from django.contrib import admin
from django.urls import path, include
from . import views

# Sentry Debug
def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_successful, name='login-view'),
    path('oauth2/', include('django_auth_adfs.urls')),

    # Sentry Debug
    path('sentry-debug/', trigger_error),
]
