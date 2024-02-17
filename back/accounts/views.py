from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, ProfileSerializer

@api_view(['GET'])
def profile(request):
    if request.method == 'GET':
    # if request.user.id != user_id:
    #     return Response(
    #         {'message': '프로필 페이지는 자기 자신만 열람 가능합니다.'},
    #         status=status.status.HTTP_400_BAD_REQUEST
    #     )

        user = get_object_or_404(User)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)




# @api_view(['GET'])
# def movie_popular(request):
#     if request.method == 'GET':
#         movies = Movie.objects.order_by('-popularity')[:10]
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)