from django.urls import path
from . import views


urlpatterns = [
    # path('reviews/', views.review_list),
    path('review_create/', views.review_create),
    path('reviews/<int:review_pk>/', views.review_detail_update_delete),
    
    path('<int:article_id>/comments/', views.comment_list),
    path('<int:article_id>/comments/<int:comment_id>/', views.comment_update_or_delete),
    
    path('<int:article_id>/article_like/', views.article_like),
]
