
from django.urls import path
from empmanage import views

urlpatterns = [
    path('register/',views.register),
    path('dashboard/',views.dashboard),
    path('dashboard/logout',views.logout),
    path('dashboard/salary/',views.view_salary),
    path('dashboard/holidays/',views.viewholidays),
    path('dashboard/leave/',views.applyforleave)
]
