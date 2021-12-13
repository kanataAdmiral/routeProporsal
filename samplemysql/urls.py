from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('rection1/', include('rection1.urls')),
    path('admin/', admin.site.urls),
]
