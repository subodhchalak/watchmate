from rest_framework.throttling import UserRateThrottle, AnonRateThrottle



class ReviewCreateThrottle(UserRateThrottle):                # throttling ReviewCreateView
    scope='reviewCreate'
    
    
# class ReviewListThrottle(UserRateThrottle):                # throttling ReviewListView
#     scope='reviews'
    