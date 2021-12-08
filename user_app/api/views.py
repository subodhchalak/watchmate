from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response

from rest_framework import status

from user_app import models

from rest_framework.authtoken.models import Token
# from rest_framework_simplejwt.tokens import RefreshToken         # To create JWT manually



@api_view(['POST',])
def logoutView(request):
    
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
def registrationView(request):
    
    if request.method == 'POST':
        serializer=RegistrationSerializer(data=request.data)
        
        data={}                                                  # creating empty dictionary
        
        if serializer.is_valid():
            account=serializer.save()                            # save method is called from serializer model
            
            
            data['response']="Registration successful!"
            
            data['username']=account.username                    # puttong data in empty dictionary
            data['email']=account.email
        
            token=Token.objects.get(user=account).key              # acccesing user token key
            data['token']=token
            
            # refresh = RefreshToken.for_user(account)              # Creating tokens manually using simple JWT
            
            # data['token']={                                          # visit Simple JWT web page for more info
            #                 'refresh': str(refresh),
            #                 'access': str(refresh.access_token),
            #             }
            
        else:
            data=serializer.errors
            
        return Response(data, status=status.HTTP_201_CREATED)