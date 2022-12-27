from django.urls import path
from .views import DataAPIListView, JobStoryAPIListView, StoryAPIListView, StoryDetailAPIView, StoryCreateAPIView, LatestItemView, UserStoryAPIListView

urlpatterns = [
    path('allstories/', DataAPIListView.as_view()),
    path('jobstories/', JobStoryAPIListView.as_view()),
    path('stories/', StoryAPIListView.as_view()),
    path('userstories/', UserStoryAPIListView.as_view()),
    path('stories/item/<int:pk>', StoryDetailAPIView.as_view()),
    path('stories/new', StoryCreateAPIView.as_view()),
    path('stories/latest/', LatestItemView.as_view())
]