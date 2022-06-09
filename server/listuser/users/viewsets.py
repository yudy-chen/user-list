import os
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.views import APIView

class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all().order_by('-id')
        serializer = UserSerializer(queryset, many=True)
        
        rb = []
        
        serverIP = request.get_host()    
        
        for user in serializer.data:
            
            photoPath = ""
            
            if user["photo_path"] != None:
                photoPath = 'http://%s/public/userphoto/%s' % (serverIP, user["photo_path"])
            
            rb.append({
                'id': user["id"],
                'userName': user["user_name"],
                'age': user["age"],
                'photoPath': photoPath
            })
        
        return Response(rb)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
        
    def destroy(self, request, pk=None):        

        try:
            user = User.objects.get(id = pk)
            user.delete()        
            return Response({'status': 'ok'})
        except Exception as e:
            return Response({'status': 'ko', 'msg' : 'User not exists'})
         
        
    def create(self, request):
        userName = request.data.get("user_name")
        
        if userName == None or userName.strip() == "":
            return Response({'status': 'ko', 'msg' : 'Username cannot be empty'})
       
        age = request.data.get("age")
        
        if age == None or age.strip() == "":
            return Response({'status': 'ko', 'msg' : 'Age cannot be empty'})
        try:
            age = int(age)
            if age < 0:
                return Response({'status': 'ko', 'msg' : 'Age is not valid'})
        except Exception as e:
            return Response({'status': 'ko', 'msg' : 'Age is not valid'})        
        
        
        user = User(user_name = userName, age = age)
        user.save()
        
        userPhoto = request.data.get("userPhoto")
        
        if userPhoto != None and userPhoto != "null":
            
            allowedTypes = ['.jpg', '.jpeg', '.png', '.gif']
            
            try:
                fileExt = os.path.splitext(userPhoto.name)[1]

                if fileExt not in allowedTypes:
                    return Response({'status': 'ko', 'msg' : 'Photo is not valid'})
                    
                photoPath = os.path.join(settings.USERPHOTO_URL, "%s%s" % (user.pk, fileExt))
                
                default_storage.save(photoPath, ContentFile(userPhoto.read()))
                
                user.photo_path = "%s%s" % (user.pk, fileExt)
                user.save()
            except Exception as e:
                return Response({'status': 'ko', 'msg' : 'Photo is not valid'})                
             
        return Response({'status': 'ok'})
        