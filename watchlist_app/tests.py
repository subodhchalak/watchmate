from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


from watchlist_app.api import serializers
from watchlist_app import models

# Create your tests here.


class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(username="example", password="password@123")
        self.token=Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream=models.StreamPlatform.objects.create(
            name="Discovery",
            about="Best Infotainement Channel",
            website="https://www.discovery.com"
        )
    
    def test_streamPlatform_create(self):
        data = {
            "name" : "Discovery",
            "about" : "Best Infotainement Channel",
            "website" : "https://www.discovery.com"   
        }
        
        response = self.client.post(reverse('streamplatform-list'), data)           # streamplatform is the basename in mentioned in router
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
          
    def test_streamPlatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamPlatform_individualElement(self):
        response=self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        
class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(username="example", password="password@123")
        self.token=Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream=models.StreamPlatform.objects.create(
            name="Discovery",
            about="Best Infotainement Channel",
            website="https://www.discovery.com",
        )
        
        self.watchlist=models.WatchList.objects.create(
            streamPlatform=self.stream,
            title="Man Vs Wild",
            storyline="Survival in toughest conditions",
            active=True,          
        )
        
       
    
    def test_watchlist_create(self):
        data = {
            "platform" : self.stream,
            "title" : "Example Movie",
            "storyline" : "Horror thriller comedy",
            "active" : True,
        }
        
        response = self.client.post(reverse('showList'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
        
    def test_wathclist_list(self):
        response=self.client.get(reverse('showList'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_wathclist_individualElement(self):
        response=self.client.get(reverse('showDetail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_watchlist_update(self):
        data = {
            "platform" : self.stream,
            "title" : "New Example Movie",
            "storyline" : "Horror thriller comedy timepass movie",
            "active" : False,
        }
        
        response=self.client.put(reverse('showDetail',  args=(self.watchlist.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_watchlist_create_unauthenticated(self):
        data = {
            "platform" : self.stream,
            "title" : "Example Movie Pro Max",
            "storyline" : "Horror thriller comedy",
            "active" : True,
        }
        
        self.client.force_authenticate(user=None)
        
        response=self.client.post(reverse('showList', ), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
        
class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(username="example", password="password@123")
        self.token=Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream=models.StreamPlatform.objects.create(
            name="Discovery",
            about="Best Infotainement Channel",
            website="https://www.discovery.com",
        )
        
        self.watchlist=models.WatchList.objects.create(
            streamPlatform=self.stream,
            title="Man Vs Wild",
            storyline="Survival in toughest conditions",
            active=True,          
        )
        
        self.watchlist2=models.WatchList.objects.create(
            streamPlatform=self.stream,
            title="Apex Predator",
            storyline="The most deadliest predators.",
            active=True,          
        )
        
        self.review=models.Review.objects.create(
            watchlist = self.watchlist2,
            review_user=  self.user,
            rating = 5,
            description = "Wild life is scary!",
            active = True,
        )
        
        
    def test_review_create(self):
        data = {
            "watchlist" : self.watchlist,
            "review_user" : self.user,
            "rating" : 5,
            "description" : "Bear Grylls is a toughest man on this planet!",
            "active" : True,            
        }
        
        response=self.client.post(reverse('reviewCreate', args=(self.watchlist.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        # self.assertEqual(models.Review.objects.get().rating, 5)
        
        response=self.client.post(reverse('reviewCreate', args=(self.watchlist.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_review_create_unauthenticated(self):
        data = {
            "watchlist" : self.watchlist,
            "review_user" : self.user,
            "rating" : 5,
            "description" : "Bear Grylls is a toughest man on this planet!",
            "active" : True,            
        }
        
        self.client.force_authenticate(user=None)
        
        response=self.client.post(reverse('reviewCreate', args=(self.watchlist.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_review_update(self):
        data = {
            "watchlist" : self.watchlist,
            "review_user" : self.user,
            "rating" : 3,
            "description" : "Wild life is ineresting. Survical of fittest!",
            "active" : False,            
        }
        
        response=self.client.put(reverse('reviewDetail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_review_list(self):
        response=self.client.get(reverse('reviews', args=(self.watchlist.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_individualElement(self):
        response=self.client.get(reverse('reviewDetail', args=(self.review.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
        
    def test_review_user(self):
        response=self.client.get(reverse('userreviews'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)       