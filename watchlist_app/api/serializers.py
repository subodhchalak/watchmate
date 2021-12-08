from django.db.models import fields
from rest_framework  import serializers

from watchlist_app.models import StreamPlatform, WatchList, Review



class ReviewSerializer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField(read_only=True)        # displaying review_user name
    
    class Meta:
        model= Review
        # fields= '__all__'
        exclude=('watchlist',)



class WatchListSerializer(serializers.ModelSerializer):
    # review=ReviewSerializer(many=True, read_only=True)
    # 'read_only' will only show 'reviews' and will not accept update data through this serializer
    
    streamPlatform=serializers.CharField(source='streamPlatform.name')
    # overiding 'streamPlatform' foreign key to display platform name instead of ID only
    
    class Meta:
        model= WatchList
        fields= "__all__"
        
        
        
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist=WatchListSerializer(many=True, read_only=True)         # Nested Serializer
    # 'watchlist' field name came from 'related_name' mentioned in 'streamPlatform' field of 'WatchList' model 
    
    class Meta:
        model= StreamPlatform
        fields= "__all__"


    
    
    
# class MovieSerializer(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField(max_length=100)
#     description=serializers.CharField(max_length=500)
#     active=serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name=validated_data.get('name', instance.name)
#         instance.description=validated_data.get('description', instance.description)
#         instance.active=validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
    
#     def validate_name(self, value):
        
#         numbers=list(range(0,10))
#         newnum=[]
        
#         for num in numbers:
#             num=str(num)
#             newnum.append(num)
        
#         for num in newnum:
#             for letter in value:
#                 if num==letter:
#                     raise serializers.ValidationError("Only Letters are allowed!")
#         return value
            
            
#     def validate_title(self, data):
#         if data['name']==data['description']:
#             raise serializers.ValidationError("Name and description should be different!")
#         return data