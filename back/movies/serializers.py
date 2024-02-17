from rest_framework import serializers
from .models import Movie, Genre, Rating

class MovieSerializer(serializers.ModelSerializer):
    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('id', 'name')
    
    # 장르 id 참조
    genre_ids = GenreSerializer(many=True, read_only=True) 


    class Meta:
        model = Movie
        # fields = ( 'title', 'vote_average', 'vote_count', 'release_date', 'poster_path', 'overview', 'popularity',)
        fields='__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('user', 'movie', 'score', 'comment')
        read_only_fields = ('user',)

       