from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import UserSerializer, UserListSerializer
from authentication.models import User

@api_view(['GET','POST'])
def UserAPI(request):

    # Listar
    if request.method == 'GET':
        users = User.objects.all().values('id','username','email','name','last_name')
        users_serializer = UserListSerializer(users, many = True)
        return Response({"users": users_serializer.data}, status = status.HTTP_200_OK)

    # Creación
    elif request.method == 'POST':    
        # Si aprueba las validaciones para el modelo de usuario, guardo en la BD o retorno algún error, de existir
        users_serializer = UserSerializer(data = request.data)
        if users_serializer.is_valid(): 
            users_serializer.save()
            user_data = users_serializer.data
            user = User.objects.get(email=user_data['email'])

            data = { "username": user.username, "email": user.email, 'name':user.name, "last_name":user.last_name, 'tokens': user.tokens()}
            return Response({"message": "user created successfully", "user": data}, status = status.HTTP_201_CREATED)
        return Response({"message": "error during user creation", "error": users_serializer.errors}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def UserDetailsAPI(request,pk=None):
    user = User.objects.filter(id=pk).first()

    if user:
        # Optener
        if request.method == 'GET':
            users_serializer = UserSerializer(user)
            return Response({"user": users_serializer.data}, status = status.HTTP_200_OK)
        
        # Actualizar
        elif request.method == 'PUT':
            users_serializer = UserSerializer(user, data= request.data)
            if users_serializer.is_valid():
                users_serializer.save()
                return Response({"message":"successful update", "user": users_serializer.data}, status = status.HTTP_200_OK)
            return Response(users_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        # Eliminiar
        elif request.method == 'DELETE':
            user.delete()
            message = f'eliminado {user.username} correctamente'
            return Response({"message": message}, status = status.HTTP_200_OK)

    return Response({'error:': 'User not found, wrong request.'}, status = status.HTTP_400_BAD_REQUEST)