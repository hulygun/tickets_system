from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', views.obtain_auth_token),
    path('docs/', include_docs_urls(title='Tickets API documentation', public=True)),
    path('api/', include('tickets.urls'))
]
