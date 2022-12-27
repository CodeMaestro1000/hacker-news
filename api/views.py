from django.http import Http404
from rest_framework import generics, status
from hackernews.models import Stories
from .serializers import GetStorySerializer, StoryCreateSerializer, StoryUpdateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from datetime import date
import string, random

# Create your views here.
class DataAPIListView(generics.ListAPIView):
    """Gets all stories - both regular stories and jobs"""
    serializer_class = GetStorySerializer

    def get_queryset(self):
        query = self.request.GET.get('order')
        print(query)
        if query == 'desc':
            return Stories.objects.all().order_by('date_added')
        return Stories.objects.all()

class JobStoryAPIListView(generics.ListAPIView):
    """Gets all job stories"""
    # queryset = Stories.objects.filter(story_type='job')
    serializer_class = GetStorySerializer

    def get_queryset(self):
        query = self.request.GET.get('order')
        if query == 'desc':
            return Stories.objects.filter(story_type='job').order_by('date_added')
        return Stories.objects.filter(story_type='job')

class StoryAPIListView(generics.ListAPIView):
    """Gets all regular stories that were pulled from hacker news"""
    # queryset = Stories.objects.filter(from_hn=True)
    serializer_class = GetStorySerializer

    def get_queryset(self):
        query = self.request.GET.get('order')
        if query == 'desc':
            return Stories.objects.filter(from_hn=True).order_by('date_added')
        return Stories.objects.filter(from_hn=True)

class UserStoryAPIListView(generics.ListAPIView):
    """Gets all stories that were created by users"""
    # queryset = Stories.objects.filter(from_hn=False)
    serializer_class = GetStorySerializer

    def get_queryset(self):
        query = self.request.GET.get('order')
        if query == 'desc':
            return Stories.objects.filter(from_hn=False).order_by('date_added')
        return Stories.objects.filter(from_hn=False)

class StoryCreateAPIView(generics.CreateAPIView):
    """Create a new story, requires the user to be authenticated"""
    serializer_class = StoryCreateSerializer
    def generate_id(self):
        chars = string.digits
        size = 6
        return int(''.join(random.choice(chars) for x in range(size)))
    
    def post(self, request):
        data = JSONParser().parse(request)
        username =  data.get('username', '')
        password = data.get('password', '')
        
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            auth_access = authenticate(request, username=username, password=password)
            if auth_access: # if username and password match
                data['id'] = self.generate_id()
                data['author'] = data['username']
                data['date_added'] = date.today()
                # remove user name and password from request payload and serialize the rest
                data.pop('username')
                data.pop('password')
                serializer = StoryCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # error if bad data is sent
        return Response({'status':'Invalid User Credentials, Check username and password again'}, status=status.HTTP_401_UNAUTHORIZED)


class StoryDetailAPIView(APIView):
    """
    Retrieve, update or delete a story instance. Also requires authentication
    """
    def get_object(self, pk):
        try:
            return Stories.objects.get(pk=pk)
        except Stories.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        story = self.get_object(pk)
        serializer = StoryUpdateSerializer(story)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        data = JSONParser().parse(request)
        username = data.get('username', '')
        password = data.get('password', '')

        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            auth_access = authenticate(request, username=username, password=password)
            if auth_access: # if username and password match
                story = self.get_object(pk)
                if story.author == username:
                    serializer = StoryUpdateSerializer(story, data=data)
                    if serializer.is_valid(): # if data to be updated is valid
                        serializer.save()
                        return Response(serializer.data)
                    else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # error if bad data is sent
                else: return Response({'status':'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({'status':'Invalid User Credentials, Check username and password again'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, format=None):
        data = JSONParser().parse(request)
        username = data.get('username', '')
        password = data.get('password', '')
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            auth_access = authenticate(request, username=username, password=password)
            if auth_access:
                story = self.get_object(pk)
                if story.author == username:
                    story.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else: 
                    return Response({'status':'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'status':'Invalid User Credentials, Check username and password again'}, status=status.HTTP_401_UNAUTHORIZED)

class LatestItemView(APIView):
    """Get the latest item in the database"""
    def get_object(self):
        try:
            return Stories.objects.latest('date_added')
        except Stories.DoesNotExist:
            raise Http404

    def get(self,request, *args, **kwargs):
        latest_id = None
        try:
            story = self.get_object()
            latest_id = story.id
            return Response({'id': latest_id}, status=status.HTTP_200_OK)
        except Stories.DoesNotExist:
            raise Http404