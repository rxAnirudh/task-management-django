from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from .models import *
from django.http import JsonResponse

# Create your views here.


@api_view(["POST"])
def signup(request):
    try:
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            email_id = serializer.data["email"]
            password = data["password"]
            role = serializer.data["role"]
            mobile_number = serializer.data["mobile_number"]
            user = UserModel.objects.filter(mobile_number=mobile_number).first()
            if user:
                userdata=list(UserModel.objects.values().filter(email=email_id))
                userdata[0].pop("password")
                userdata[0].pop("is_active")
                userdata[0].pop("is_delete")
                userdata[0].pop("user_id")
                return Response({"successs" : False,"data" : userdata[0],"message":"Profile already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_user = UserModel.objects.create(first_name=first_name,last_name=last_name,email=email_id,mobile_number=mobile_number,password=password,role=role)
            new_user.save()
            userdetails =list(UserModel.objects.values().filter(id=new_user.id))
            print("userdetails")
            print(userdetails)
            userdetails[0].pop("is_active")
            userdetails[0].pop("is_delete")
            return Response({"successs" : True,"data" : userdetails[0],"message":"User created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def signin(request):
    try:
        data = request.data
        serializer = SignInSerializer(data=data)
        if serializer.is_valid():
            password = serializer.data["password"]
            email = serializer.data["email"]
            user = UserModel.objects.filter(email=email,password=password).first()
            if not user:
                return Response({"successs" : False,"message":"Account does not exists, please register first"}, status=status.HTTP_201_CREATED)
            userdata=list(UserModel.objects.values().filter(email=email))
            userdata[0].pop("password")
            userdata[0].pop("is_active")
            userdata[0].pop("is_delete")
            userdata[0].pop("user_id")
            return JsonResponse({"successs" : True,"data" : userdata[0],"message":"User logged in successfully"}, safe=False)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)