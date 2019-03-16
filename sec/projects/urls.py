from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProjectsView.as_view(), name='projects'),
    path('new/', views.new_project, name='new_project'),
    path('<int:project_id>/', views.project_view, name='project_view'),
    path('<int:project_id>/tasks/<int:task_id>/', views.task_view, name='task_view'),
    path('<int:project_id>/tasks/<int:task_id>/upload/', views.upload_file_to_task, name='upload_file_to_task'),
    path('<int:project_id>/tasks/<int:task_id>/permissions/', views.task_permissions, name='task_permissions'),
    path('delete_file/<int:file_id>', views.delete_file, name='delete_file'),
    path('uploads/tasks/<int:task_id>/<file>', login_required(views.TaskFileDownloadView.as_view())),
    path('uploads/deliveries/<int:task_id>/<file>', login_required(views.DeliveryFileDownloadView.as_view())),
]
#(?P<path>.*)$
