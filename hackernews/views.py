from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Stories, Comments
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime
import string, random
from pytz import timezone

# Create your views here.
class HomePageView(ListView):
    model =  Stories
    template_name = 'home.html'
    context_object_name = 'stories'
    paginate_by = 20

class StoryDetailView(DetailView):
    model = Stories
    template_name = 'story_detail.html'
    context_object_name = 'story'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.comment_tree = {}

    def create_comment_structure(self, parent):
        if parent.kids:
            children = Comments.objects.filter(parent_id=parent.id).all()
            self.comment_tree[parent.id] = {'text': parent.text, 'author': parent.author, 'kids': [], 'date':parent.date_added}
            for child in children:
                self.comment_tree[parent.id]['kids'].append(child.id)
                self.create_comment_structure(child)
        else: 
            self.comment_tree[parent.id] = {'text': parent.text, 'author': parent.author, 'date':parent.date_added}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        story_comments = Comments.objects.filter(parent_id=self.kwargs.get('pk')).all()
        for comment in story_comments:
            self.create_comment_structure(comment)
        context.update({'comment_data': self.comment_tree})
        return context
        
class FilterResultView(ListView):
    model = Stories
    context_object_name = 'story_list'
    template_name = 'story_filter.html'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Stories.objects.filter(story_type=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'query_data':self.request.GET.get('q')})
        return context

class SearchResultView(ListView):
    model = Stories
    context_object_name = 'story_list'
    template_name = 'search_results.html'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Stories.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))

class UserStoryListView(LoginRequiredMixin, ListView):
    model = Stories
    paginate_by = 20
    template_name = 'user_story.html'
    context_object_name = 'story_list'

    def get_queryset(self):
        return Stories.objects.filter(author=self.request.user.username)


class StoryCreateView(LoginRequiredMixin, CreateView):
    model = Stories
    template_name = 'new_story.html'
    fields = ['title', 'url', 'text']

    def generate_id(self):
        chars = string.digits
        size = 6
        return int(''.join(random.choice(chars) for x in range(size)))

    """Populate hidden form fields before savinf to db"""
    def form_valid(self, form): 
        form.instance.id = self.generate_id()
        form.instance.author = self.request.user.username 
        form.instance.date_added = datetime.now(tz=timezone('UTC'))
        return super().form_valid(form)


class StoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Stories
    template_name = 'story_delete.html'
    success_url = reverse_lazy('home') 

    """Function to validate deleting data based on source of data and user authorization"""
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user.username and obj.from_hn == False

class StoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Stories
    template_name = 'story_edit.html'
    fields = ['title', 'url', 'text']

    """Function to validate updating data based on source of data and user authorization"""
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user.username and obj.from_hn == False
    