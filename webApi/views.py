from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import *
from .models import *
from .Useable import token as _auth
from .Useable import permission as perm

class UserAuthViewset(ModelViewSet):
    # User SignUp 
    @action(detail=False, methods=['POST'])
    def userSignup(self, request):
        try:
            email= request.data.get("email")
            password= request.data.get("password")
            if not email and not password:
                return Response({"status": False, "message": "email and password both required" }, status=status.HTTP_400_BAD_REQUEST)
            ser = UserSignupSerializer(data= request.data)
            if ser.is_valid():
                ser.save()
                return Response ({"status": True, "message" : "User created !!!" }, status=status.HTTP_201_CREATED)
            return Response({"status": False, "message": ser.errors }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response ({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # User Login
    @action(detail=False, methods=['POST'])
    def userLogin(self, request):
        try:
            email= request.data.get("email")
            password= request.data.get("password")
            if not email and not password:
                return Response({"status": False, "message": "email and password both required" }, status=status.HTTP_400_BAD_REQUEST)
            ser = UserLoginSerializer(data= request.data)
            if ser.is_valid():
                fetchuser = ser.validated_data['fetch_user']
                user_token = _auth.UserGenerateToken(fetchuser)
                if user_token['status']:
                    return Response({"status": True, "msg": "Login Successfully", "token": user_token['token'], "payload": user_token['payload']}, status= 200)
                return Response ({"status": False, "message": f"Invalid Credentials {user_token['message']}"}, status= 400)
            
            return Response({"status": False, "msg" : ser.errors}, status= 400)
        except Exception as e:
            return Response ({"status": False, "error": str(e)}, status= 400)


class ChatAPIView(APIView):
    permission_classes = [perm.UserPermission]
    def post(self, request):
        user= request.auth['id']
        request.data['created_by']= user
        serializer = ChatsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":True, "message":"chat created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"status":False, "message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        chats = Chats.objects.all()
        serializer = ChatsSerializer(chats, many=True)
        return Response({"status":True, "chats_data":serializer.data}, status= 200)

class MessageAPIView(APIView):
    permission_classes = [perm.UserPermission]
    def get(self, request):
        chat_id= request.GET.get('chat_id')
        if not chat_id:
            return Response ({"status": False, "message": "chat_id must be require . . ."})
        messages = Message.objects.filter(chatid= chat_id)
        serializer = GetMessageSerializer(messages, many=True)
        return Response({"status":True, "messages":serializer.data}, status=200)

    def post(self, request):
        user= request.auth['id']
        request.data['user']= user
        print(request.data)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":True, "message":"message created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)