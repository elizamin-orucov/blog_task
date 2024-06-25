## Django Blogger Blogs
#### 
You can use the blog project I made as per your wishes.

## Description

The purpose of the Blogger project is for people to share blogs and to be able to read and like other people's blogs easily.
I used the Jinja template engine as the template language in the project. I built the backend with Python's Django framework.

## Installation
````bash
git clone https://github.com/elizamin-orucov/blog_project.git .
pip install -r requirements.txt
django-admin startproject core .
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
````