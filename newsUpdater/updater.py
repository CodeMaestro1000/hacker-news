from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from newsUpdater.getter import get_stories

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_stories, 'interval', minutes=2)
    scheduler.start()