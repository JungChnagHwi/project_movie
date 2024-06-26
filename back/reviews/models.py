from django.db import models
from django.conf import settings

class Review(models.Model):
    movie_title = models.CharField(max_length=100)
    article_title = models.CharField(max_length=100)
    article_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(null=True, max_length=50)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rated_reviews')
    rating = models.IntegerField(null=True, default=1, choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')])

    class Meta:
        ordering = ['-pk', ]

    def __str__(self):
        return self.article_title


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Review, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(null=True, max_length=50)

    class Meta:
        ordering = ['-pk', ]

    def __str__(self):
        return self.content