from django.db import models
from django.db.models.aggregates import Min
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import User


# Create your models here.


class StreamPlatform(models.Model):
    name=models.CharField(max_length=100)
    about=models.TextField(max_length=500)
    website=models.URLField(max_length=100)
    
    def __str__(self):
        return self.name
    
    

class WatchList(models.Model):
    streamPlatform=models.ForeignKey(StreamPlatform, default=None, on_delete=models.CASCADE, related_name='watchlist',)
    
    title=models.CharField(max_length=100)
    storyline=models.TextField(max_length=500)
    active=models.BooleanField(default=True)           # if movie/series is launched
    created=models.DateTimeField(auto_now_add=True)    # current DateTime field
    
    number_rating=models.IntegerField(default=0)
    avg_rating=models.FloatField(default=0)
    
    
    def __str__(self):
        return (f"{self.streamPlatform} | {self.title}")
    
    
class Review(models.Model):
    watchlist=models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='review')
    review_user=models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='review_user')
    
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description=models.TextField(max_length=500, null=True, blank=True)
    active=models.BooleanField(default=True,)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return (f"{self.watchlist} | {self.rating}  |   {self.review_user}")
    
    
    
    
    
