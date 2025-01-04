from django.urls import path
from . import views

app_name = 'regression_project'

urlpatterns = [
    path('create/', views.ProjectStageOneView.as_view(), name='create_project'),
    path('create/stage2/', views.ProjectStageTwoView.as_view(), name='create_project_stage_two'),
    path('', views.IndexView.as_view(), name='index'),
]
