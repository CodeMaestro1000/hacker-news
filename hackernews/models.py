from django.db import models
from django.urls import reverse

# Create your models here.
# model structure:
# two tables: Stories  and Comments

class Stories(models.Model):
    id = models.BigIntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=2000, null=False)
    text = models.TextField(blank=True, default='')
    date_added = models.DateTimeField(null=False)
    author = models.CharField(max_length=200, null=False)
    url = models.CharField(max_length=200, null=False, blank=True, default='')
    score = models.IntegerField(null=False, default=0)
    kids = models.BooleanField(null=False, default=False)
    story_type = models.CharField(max_length=20, null=False, default='story')
    from_hn = models.BooleanField(null=False, default=False) # from hacker news

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title[:50]

    def get_absolute_url(self): # new
        return reverse('story_detail', args=[str(self.id)])


class Comments(models.Model):
    story = models.ForeignKey(Stories, on_delete=models.CASCADE, related_name='comments')
    id = models.BigIntegerField(primary_key=True)
    parent_id = models.BigIntegerField(null=False)
    author = models.CharField(max_length=200, null=False)
    date_added = models.DateField(null=False)
    kids = models.BooleanField(null=False, default=False)
    text = models.CharField(max_length=4000, null=False)

    

