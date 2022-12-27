from django.urls import path
from .views import HomePageView, StoryDetailView, FilterResultView, SearchResultView, StoryCreateView, StoryDeleteView, StoryUpdateView, UserStoryListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('story/<int:pk>/', StoryDetailView.as_view(), name='story_detail'),
    path('story/<int:pk>/delete/', StoryDeleteView.as_view(), name='delete_story'),
     path('story/<int:pk>/edit/', StoryUpdateView.as_view(), name='edit_story'),
    path('story/new/', StoryCreateView.as_view(), name='new_story'),
    path('filters/', FilterResultView.as_view(), name='filter_results'),
    path('search/', SearchResultView.as_view(), name='search_results'),
    path('mystories/',UserStoryListView.as_view(), name='user_stories')
]