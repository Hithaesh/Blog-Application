from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.Serializer):
  first_name = serializers.CharField()
  last_name = serializers.CharField()

  username = serializers.CharField(max_length = 100)
  password = serializers.CharField(write_only = True) # write_only will not be included in the serialized response data
  confirm_password = serializers.CharField(write_only = True) # Remember to POP from the data when creation

  def validate(self, data):
    # Check-1: Check if the USERNAME is already present in the USER model
    if User.objects.filter(username = data.get('username')).exists():
      raise serializers.ValidationError("Username already Exists!")
    
    if len(data.get('username')) < 3 or len(data.get('username')) > 100:
      raise serializers.ValidationError("Username is less than 3 or greater than 100")
    
    if data.get('password') !=  data.get('confirm_password'):
      raise serializers.ValidationError("Password doesn't match with Confirm Password")

    return data
  
  def create(self, validated_data):
    # Popping the "confirm_password" as it was only required for VALIDATION
    validated_data.pop('confirm_password')
    
    user = User.objects.create_user(
      username = validated_data.get('username').lower(),
      password = validated_data.get('password')
    )

    return user
  

class LoginSerialize(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()

  def validate(self, data):

    # Check for username is valid
    user = User.objects.filter(username = data.get('username')).first()
    if not user:
      raise serializers.ValidationError("Username is not Registered!")
    
    return user
  
  def get_jwt_token(self, data):

    user = authenticate(username = data['username'], password = data['password'])

    if not user:
      return {'message': "Invalid credentails", "data": {}}
      
    refresh = RefreshToken.for_user(user)

    return {'message': "Login Success", 'data': {'token' : {'refresh' : str(refresh), 'access': str(refresh.access_token)}}}
    





