from rest_framework import serializers
from hackernews.models import Stories


class GetStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = ('id', 'title', 'author', 'text', 'date_added', 'url', 'score', 'kids', 'story_type', 'from_hn')

class StoryCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=2000)
    text = serializers.CharField(allow_blank=True, required=False)
    date_added = serializers.DateField()
    author = serializers.CharField(max_length=200)
    url = serializers.CharField(max_length=200, allow_blank=True, required=False)
    story_type = serializers.CharField(max_length=20, required=False)
    from_hn = serializers.BooleanField(required=False) # from hacker news

    def create(self, validated_data):
        """
        Create and return a new `Story` instance, given the validated data.
        """
        return Stories.objects.create(**validated_data)

class StoryUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=2000, required=False)
    text = serializers.CharField(allow_blank=True, required=False)
    url = serializers.CharField(max_length=200, allow_blank=True, required=False)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Story` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.url = validated_data.get('url', instance.url)
        instance.save()
        return instance