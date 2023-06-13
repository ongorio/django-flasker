from django.urls import path
from publications import views

app_name = 'publications'

urlpatterns = [
    path('', views.PublicationsListView.as_view(), name='publications'),
    path('create/', views.PublicationCreateView.as_view(), name='publication_create'),
    path('<int:pk>/', views.PublicationDetailView.as_view(), name='publication_detail'),
    path('<int:pk>/edit/', views.PublicationEditView.as_view(), name='publication_update'),
    path('<int:pk>/delete/', views.PublicationDeleteView.as_view(), name='publication_delete'),
    path('<int:pubId>/comment-create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('<int:Id>/comment-delete/', views.CommentDeleteView.as_view(), name='comment_delete')
]
