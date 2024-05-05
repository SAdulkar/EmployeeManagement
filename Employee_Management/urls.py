
from django.contrib import admin
from django.urls import path,include
from empmanage import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('employee/',include('empmanage.urls')),
    path('hr/',include('humanresource.urls'))
]
