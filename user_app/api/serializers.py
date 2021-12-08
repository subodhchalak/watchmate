from django.contrib.auth.models import User

from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type': 'password'}, write_only=True)           # user can not read it, only write it..
    # this field is not defined in User model so defining exlusively
    
    class Meta:
        model=User
        fields=['username', 'email', 'password', 'password2']
        
        extra_kwargs={
            'password':{'write_only': True}       # making password field write only
        }
        
        
    def save(self):
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        
        if password!=password2:
            raise serializers.ValidationError({"Error":"Password mismatch"})  
        
        email_check=User.objects.filter(email=self.validated_data['email'])        # checking email already exsts
        if email_check.exists():
            raise serializers.ValidationError({"Error": "Email already exists"})
        
        username_check=User.objects.filter(username=self.validated_data['username']) # checking username already exists
        if username_check.exists():
            raise serializers.ValidationError({"Error": "Username already exists"})
        
        account=User(username=self.validated_data['username'], email=self.validated_data['email'])
        account.set_password(self.validated_data['password'])
        account.save()
        
        return account