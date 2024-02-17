from django.urls import path
from movies import views



app_name = 'movies'
urlpatterns = [
    path('', views.index),
    path('toprated/', views.movie_toprated),
    path('popular/', views.movie_popular),
    path('recent/', views.movie_recent),
    path('genre/', views.movie_genre),
    path('commingsoon/', views.movie_commingsoon),
   
    path('lang/', views.movie_lang),
    path('company/', views.movie_company),
    path('country/', views.movie_country),
    
    path('<int:movie_id>/movie_like/', views.movie_like),
    path('<int:movie_id>/rating/', views.movie_rating),
    #  # 새로 작성 
    # path('<int:movie_pk/likes/', views.likes, name='likes'),
    
]