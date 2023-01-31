# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import requests
import os


@blueprint.route('/index')
@login_required
def index():
    url = "http://host.docker.internal:8000/reddit/submissions?query=wd-40&limit=100"
    
    payload={}
    headers = {
      'Accept': 'application/json',
      'Accept-Encoding': 'gzip, deflate',
      'Host': 'host.docker.internal:8000',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15',
      'Accept-Language': 'en-US,en;q=0.9',
      'Referer': 'http://host.docker.internal:8000/docs',
      'Connection': 'keep-alive'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    
    posts = response.json()['results']
    return render_template('home/index.html', segment='index', posts=posts)

@blueprint.route('/post')
@login_required
def post_detail():
    _id = request.args.get('_id')
    url = "http://host.docker.internal:8000/reddit/submissions?_id={}".format(_id)
    
    payload={}
    headers = {
      'Accept': 'application/json',
      'Accept-Encoding': 'gzip, deflate',
      'Host': 'host.docker.internal:8000',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15',
      'Accept-Language': 'en-US,en;q=0.9',
      'Referer': 'http://host.docker.internal:8000/docs',
      'Connection': 'keep-alive'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    
    post = response.json()['results'][0]
    return render_template('home/post.html', segment='index', post=post)


@blueprint.route('/reddit_callback')
@login_required
def reddit_callback():
    # extract code and state from query string
    username = request.args.get('username')
    read_only = request.args.get('read_only')
    
    return render_template('home/reddit_callback.html', username=username, read_only=read_only)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
