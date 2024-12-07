from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PublicationListView.as_view(), name='index'),
    path('publication/<int:pk>', views.PublicationDetailView.as_view(), name='publication_detail'),
    path('publication/<int:id>/comments/', views.AddCommentView.as_view(), name='add_comment'),
]