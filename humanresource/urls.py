
from django.urls import path
from humanresource import views
urlpatterns = [
    path('login/',views.login),
    path('register/',views.register),
    path('logout/',views.logout),
    path('dashboard/',views.dashboard),
    path('dashboard/view',views.view_employee),
    path('dashboard/view/edit/',views.edit_emp_profile),
    path('dashboard/view/delete',views.delete_emp),
    path('dashboard/salary/',views.salary),
    path('dashboard/viewprofile/',views.viewprofile),
    path('dashboard/leave/',views.leave_request_status),
    path('dashboard/leave/accept/',views.accept_leave),
    path('dashboard/leave/reject/',views.reject_leave),

]
