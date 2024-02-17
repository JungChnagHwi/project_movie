from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Movie, Rating
from .serializers import MovieSerializer, GenreSerializer, RatingSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
import requests
from django.conf import settings
import json
from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.models import User



#모든 데이터 추출
@api_view(['GET'])
def index(request):
    if request.method == 'GET':
        movies = Movie.objects.order_by('-popularity')[:500]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    

    

#평점순
@api_view(['GET'])
def movie_toprated(request):
    if request.method == 'GET':
        # vote_count가 1000 이상인 영화들만 필터링
        movies = Movie.objects.filter(vote_count__gte=1000).order_by('-vote_average')[:20]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


# 인기순
@api_view(['GET'])
def movie_popular(request):
    if request.method == 'GET':
        movies = Movie.objects.order_by('-popularity')[:20]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

# 최신
@api_view(['GET'])
def movie_recent(request):
    if request.method == 'GET':
        current_date = datetime.now().date()
        movies = Movie.objects.filter(release_date__lt=current_date, vote_count__gte=100).order_by('-release_date')[:20]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
#comingsoon
@api_view(['GET'])
def movie_commingsoon(request):
    if request.method == 'GET':
        current_date = datetime.now().date()
        next_day = current_date + timedelta(days=1)
        movies = Movie.objects.filter(release_date__gte=next_day).order_by('-vote_count')[:20]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
# 장르
@api_view(['GET'])
def movie_genre(request):
    if request.method == 'GET':
        genre_ids_str = request.query_params.get('genre_ids', '')
        genre_ids = [int(genre_id) for genre_id in genre_ids_str.split(',') if genre_id.isdigit()]

        movies = Movie.objects.filter(genres__pk__in=genre_ids).order_by('-popularity')[:20]

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    

#언어
@api_view(['GET'])
def movie_lang(request):
    if request.method == 'GET':
        selected_language = request.GET.get('language', 'ko')  
        movies = Movie.objects.filter(original_language=selected_language, vote_count__gte=750, vote_average__gte=7.5).order_by('-popularity')[:20]
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)
    
#회사별
@api_view(['GET'])
def movie_company(request):
    if request.method == 'GET':
        selected_company = request.GET.get('company', 'Walt Disney Pictures')  # 기본값으로 'Warner Bros. Pictures'를 설정했습니다.
        movies = Movie.objects.filter(companies__icontains=selected_company).order_by('-popularity')[:20]

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

#나라별
@api_view(['GET'])
def movie_country(request):
    if request.method == 'GET':
        selected_country = request.GET.get('country', 'All Countries')

        # 'All Countries'가 선택된 경우 모든 영화를 반환
        if selected_country == 'All Countries':
            movies = Movie.objects.filter(vote_count__gte=200, vote_average__gte=7.5).all().order_by('-popularity')[:1000]
        else:
            # 선택된 나라에 해당하는 영화만 필터링
            movies = Movie.objects.filter(country__icontains=selected_country, vote_count__gte=200, vote_average__gte=7.5).order_by('-popularity')[:1000]

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_like(request, movie_id):
    
        movie = Movie.objects.get(pk=movie_id)
        if request.user in movie.like_users.all():
            movie.like_users.remove(request.user)
        else:
            movie.like_users.add(request.user)

        return Response({'movie_id': movie_id}, status=status.HTTP_200_OK)

    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_rating(request, movie_id):
    user = request.user
    data = {'user': user.id, 'movie': movie_id, **request.data}
    serializer = RatingSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


