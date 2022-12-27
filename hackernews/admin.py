from django.contrib import admin
from .models import Stories, Comments

# Register your models here.
class CommentInline(admin.StackedInline):
    model = Comments
    extra = 0

class StoryAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

admin.site.register(Stories, StoryAdmin)