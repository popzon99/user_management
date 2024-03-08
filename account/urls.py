from django.urls import path
from .views import CustomLoginView, CustomRegistrationView, StudentDashboardView, StaffDashboardView, AdminDashboardView, EditorDashboardView,index,logout_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegistrationView.as_view(), name='register'),
    path('student/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('staff/', StaffDashboardView.as_view(), name='staff_dashboard'),
    path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('editor/', EditorDashboardView.as_view(), name='editor_dashboard'),
    path('',index, name = 'index'),
    path('logout/', logout_view, name='logout'),
    
]
