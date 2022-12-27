# Introduction
Hacker News (HN) Feed is a web application that sources news and job postings from hackernews.com

Users of HN feed can view stories and comments from hacker news directly on their HNFeed Dashboard

# Usage
HNFeed has been developed as a web app using django. Users can view stories without logging in but you have to be logged in to post your own stories.

The app (using the APScheduler package) periodically fetches data (every 5 minutes) from hackernews via api requests (as a background task). This data can be accessed via the web app or programatically using API requests and this data is saved to HNFeed's database.

Each User created story can be edited or deleted altogether.

Run initial startup code (or include in deployment script) to get first batch of fresh hacker news:
```
python manage.py startup
```

Start server with command:
```
python manage.py runserver --noreload
```

`--noreload` flag ensures that the server isn't spun up twice which is the default behaviour in debug mode.

# Containers
To remove the need for replicating the dev/prod environment, the application has been containerized using docker and docker-compose. This is the recommended way to run the app. However, note that you have to have docker installed. You can view the installation guide [here](https://docs.docker.com/engine/install/)

If you have docker installed, you can run the following commands in the root directory of this project (where you have the Dockerfile) to get the server up and running:
```
docker build .
```
Then run the container in detached mode:
```
docker-compose up -d
```

And then to setup the database for the very first time (this command should only be run the first time the image is built):
```
docker-compose exec web python manage.py migrate
```

Once the container is running, you can visit the homepage: http://localhost:8000/. You wouldn't see any data just yet because the data is pulled every 2 minutes. Refresh the page after 4 minutes (take into account the time it takes to pull the data) and then voila!

You can also try out the API endpoints using postman or whatever tool you like.

# API Endpoints
- GET http://localhost:8000/api/v1/allstories returns all stories from HNFeed's database
- GET http://localhost:8000/api/v1/jobstories returns all hackernews job stories from HNFeed's database
- GET http://localhost:8000/api/v1/stories returns all stories sourced from hacker news
- GET http://localhost:8000/api/v1/userstories returns all stories created by HNFeed users.
- POST http://localhost:8000/api/v1/stories/new adds a new story to the database. Requires authorization.
    - Example Usage:
    ```
    url = 'http://localhost:8000/api/v1/stories/new'
    data = {'username':'username', 'password':'password'}
    r = requests.delete(url, json=data)
    print(r.status_code)
    print(r.json())
    ```
- GET http://localhost:8000/stories/item/{item_id} returns a story matching the item id
- PUT http://localhost:8000/stories/item/{item_id} updates story data matching the item id. Requires authorization.
    - Example Usage: 
    ```
    url = 'http://localhost:8000/stories/item/1234'
    data = {'username':'username', 'password':'password', 'title':'updated title'}
    r = requests.put(url, json=data)
    print(r.status_code)
    print(r.json())
    ```
- DELETE  http://localhost:8000/stories/item/{item_id} deletes the story data matching the item id. Requires authorization.
    - Example Usage: 
    ```
    url = 'http://localhost:8000/stories/item/1234'
    data = {'username':'username', 'password':'password'}
    r = requests.delete(url, json=data)
    print(r.status_code)
    print(r.json())
    ```
- GET http://localhost:8000/stories/latest returns the newest item added to the db. For notifying users of new posts on the frontend.

## Sorting
All endpoints that return multiple stories can be prefixed with an order parameter. Passing `desc` as the value will return the data from oldest to newest.
The default is that the data is returned from newest to oldest. Passing any other value other than `desc` will result in the data being returned in the default order.
- Example Usage:
    ```
    url = 'http://localhost:8000/api/v1/allstories?order=desc' # returns stories from oldest to newest
    r = requests.get(url)
    print(r.status_code)
    print(r.json())
    ```

# Schema
Paste the following url in your browser to view the swagger/openAPI documentation for the HNFeed API: http://localhost:8000/api_schema

# Database
The project uses the Postgresql (v11) database. This database runs with Django's ORM using pyscopg-binaries (this package makes porting sqlite databases to postgres seamless).

# Code
The project consists of a monolith application and an API. The code for the monolith can be found in the `hackernews` directory while the API code can be found in `api`.

The `newsUpdater` directory contains the code used to fetch hackernews data to HNFeed's database periodically.

The `accounts` directory contains the code that manage users activities. Much of the user system has been abstracted away using django's built-in user model so you won't find much code there.

The `config` directory contains the configuration files used for setting up the database, middleware, static files etc.

# Thank you
Thanks for reading and I hope you enjoy testing out this application.
