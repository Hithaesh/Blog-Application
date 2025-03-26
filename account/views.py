from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer


class RegisterView(APIView):
  def post(self, request):
    try:
      registered_data = request.data

      serializer = RegisterSerializer(data = registered_data)

      if not serializer.is_valid():
        return Response({
          "data": serializer.errors,
          "message": "Something went wrong!"
        }, status= status.HTTP_400_BAD_REQUEST)
      
      serializer.save() 
      # Deserialize serialize = serialize.save()

      print(serializer.data)

      return Response({
        "message": "Successfully Registered!",
        "data": {
          "firstName": serializer.validated_data['first_name'],
          "lastName": serializer.validated_data['last_name'],
          "username": serializer.validated_data['username']
        }
      }, status=status.HTTP_200_OK)

    except Exception as e:
      print(e)
      return Response({
        "data": str(e),
        "message": "Inside Exception Block"
      }, status= status.HTTP_400_BAD_REQUEST)
