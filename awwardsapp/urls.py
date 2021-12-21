from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name = 'index'),
    path('profile/', views.profile, name='profile'),
    path('new/project/', views.new_project, name='newProject'),
    path('search/', views.search, name='search_results'),
    path('rate/<int:id>',views.rate, name='rating'),
    path("project/<int:project_id>/", views.project_review, name="project_review"),
    path('api/project/', views.ProjectList.as_view()),


]