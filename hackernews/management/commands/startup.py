from django.core.management.base import BaseCommand, CommandError
import requests
from hackernews.models import Stories, Comments
from datetime import datetime
from pytz import timezone
import logging

logging.basicConfig(level=logging.INFO)

"""Recursive function to traverse tree-like comment structure from hacker news"""
def traverse_comments(parent_id, item_id, story):
    url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json?print=pretty"
    res = requests.get(url)
    data = res.json()
    try:
        kids = data.get('kids')
        has_kids = True if kids else False
        date = datetime.fromtimestamp(data['time'], tz=timezone('UTC'))
        comment = Comments(story=story, id=data['id'], parent_id=parent_id, author=data['by'], date_added=date, kids=has_kids, text=data['text'])
        comment.save()
    except KeyError:
        logging.info(f"*********** Error for {item_id}, see {url} ***********")
    if 'kids' in data.keys():
        for child_id in data['kids']:
            traverse_comments(data['id'], child_id, story)

""" Run with shell comand 'python manage.py startup' """
class Command(BaseCommand):
    help = "Intial Loading from hacker news into DB"

    """Run Once on Startup"""
    def handle(self, *args, **kwargs):
        try:
            logging.info("Getting Story Data from hacker news...")
            url = "https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty"
            res = requests.get(url)
            new_stories = res.json()[:100]
            
            for story_id in new_stories:
                url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
                res = requests.get(url)
                data = res.json()
                has_kids = True if data.get('kids') else False
                date = datetime.fromtimestamp(data['time'], tz=timezone('UTC'))
                url = data.get('url', 'None')
                story = Stories(
                    id=data['id'], author=data['by'], title=data['title'], url=url,
                    score=data['score'], kids=has_kids, from_hn=True, date_added=date
                    )
                story.save()
                if has_kids:
                    print("\tGetting Comments....")
                    for child_id in data['kids']:
                        traverse_comments(story_id, child_id, story)
            logging.info("Done...")

            logging.info("Getting Job stories...")
            url = "https://hacker-news.firebaseio.com/v0/jobstories.json?print=pretty"
            res = requests.get(url)
            new_stories = res.json()[:100]
            
            for story_id in new_stories:
                url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
                res = requests.get(url)
                data = res.json()
                has_kids = True if data.get('kids') else False
                date = datetime.fromtimestamp(data['time'], tz=timezone('UTC'))
                url = data.get('url', 'None')
                story = Stories(
                    id=data['id'], author=data['by'], title=data['title'], url=url,
                    score=data['score'], kids=has_kids, from_hn=True, date_added=date,
                    story_type=data['type']
                    )
                story.save()
                if has_kids:
                    logging.info("\tGetting Comments....")
                    for child_id in data['kids']:
                        traverse_comments(story_id, child_id, story)
            logging.info("Done...")
        except CommandError as e:
            raise CommandError(e)