from django.db import models
from django.conf import settings

class Genre(models.Model):
    genre_id = models.IntegerField(unique=True)
    genre_name = models.CharField(max_length=50)

    def __str__(self):
        return self.genre_name

# class Country(models.Model):
#     country_code = models.IntegerField(unique=True)
#     country_name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.country_name
    
# class Company(models.Model):
#     company_id = models.IntegerField(unique=True)
#     company_name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.company_name

class Movie(models.Model):
    movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=100, null=True)
    release_date = models.DateField(null=True)
    popularity = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    vote_average = models.FloatField(null=True)
    overview = models.TextField(null=True, blank=True)
    poster_path = models.CharField(max_length=200, null=True)
    genres = models.ManyToManyField(Genre , related_name='movies', blank=True)
    runtime = models.IntegerField(null=True)
    tagline = models.TextField(null=True, blank=True)
    revenue = models.IntegerField(null=True)
    budget = models.IntegerField(null=True)
    countries = models.CharField(max_length=500, null=True, blank=True)
    # homepage = models.TextField(null=True, blank=True)
    companies = models.CharField(max_length=500, null=True, blank=True)
    original_language = models.TextField(null=True, blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rated_movies')
    video_url = models.CharField(max_length=1000, null=True, blank=True)
    director = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f'{self.title}:{self.genres}'


    def __str__(self):
        return f'{self.user.username} - {self.movie.title} (Like)'
    
class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings_user')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings', null=True)
    score = models.FloatField()  # 별점
    comment = models.CharField(max_length=300, blank=True, null=True)  # 댓글
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'movie']

    def __str__(self):
        return f'{self.user.username} - {self.movie.title} (Rating)'