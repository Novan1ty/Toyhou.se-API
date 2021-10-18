# Toyhou.se - API | Python ~ 10/12/21; October 12, 2021

"""
Started on: 10/12/21; October 12, 2021
Finished on: 10/18/21; October 18, 2021
"""

from flask import Flask, request, render_template
import requests as Request
from bs4 import BeautifulSoup

App = Flask('app', template_folder='Template', static_url_path='/Template', static_folder='Template')

Title = 'Toyhou.se | API'
Description = 'Tired from copy and pasting characters\' information? Well i got ya, an API for Toyhou.se'

Characters_URL = { 'message': 'You have to provide a character\'s url' }

@App.route('/')
def Toyhouse():
    # return {
    #     'Toyhou.se': [
    #         '/creator?url='
    #     ]
    # }

    return render_template(
        'index.html', Title=Title,
        Description=Description
    )

@App.route('/creator')
def Creator():
    URL = request.args.get('url')
    if not URL:
        return Characters_URL

    # return url

    if 'https://toyhou.se/' not in URL:
        return Characters_URL

    Character = Request.get(URL).text
    # return Character

    Toyhouse = BeautifulSoup(Character, 'lxml')

    Creator = Toyhouse.find('span', 'display-user')
    # Creator_Username = Toyhouse.find('span', class_='display-user-username')
    # Creator_Avatar = Toyhouse.find('img', class_='display-user-avatar')

    Creator_URL = Creator.a['href']
    Username = Creator.a.span.text
    Avatar = Creator.a.img['src']

    return {
        'URL': Creator_URL,
        'Username': Username,
        'Avatar': Avatar
    }

@App.route('/character')
def Character():
    URL = request.args.get('url')
    if not URL or 'https://toyhou.se/' not in URL:
        return Characters_URL

    Character = Request.get(URL).text
    Toyhouse = BeautifulSoup(Character, 'lxml')

    Character = Toyhouse.find('span', 'display-character').a
    Name = Character.text
    Avatar = Character.img['src']

    return { 'Name': Name, 'Avatar': Avatar }

@App.route('/profile')
def Profile():
    URL = request.args.get('url')
    if not URL or 'https://toyhou.se/' not in URL:
        return Characters_URL

    Character = Request.get(URL).text
    Toyhouse = BeautifulSoup(Character, 'lxml')

    Character_Profile = Toyhouse.find('div', 'profile-content-content')

    Profile = []
    for Info in Character_Profile:
        Info = Info.text
        if Info != '\n':
            Profile.append(Info)
    
    while '' in Profile:
        Profile.remove('')
    return { 'Profile': Profile }

@App.route('/gallery')
def Gallery():
    URL = request.args.get('url')
    if not URL or 'https://toyhou.se/' not in URL:
        return Characters_URL

    Character = Request.get(URL + '/gallery').text
    Toyhouse = BeautifulSoup(Character, 'lxml')

    Gallery = []

    Images = Toyhouse.find_all('li', 'gallery-item')
    for Image in Images:
        Image = Image.div.div.a['href']
        Gallery.append(Image)

    return { 'Gallery': Gallery }

@App.route('/creation')
def Creation():
    URL = request.args.get('url')
    if not URL or 'https://toyhou.se/' not in URL:
        return Characters_URL
    
    Character = Request.get(URL).text
    Toyhouse = BeautifulSoup(Character, 'lxml')

    Creation = Toyhouse.find('abbr', 'tooltipster')
    Created = Creation.text
    Date_n_Time = Creation['title']

    return { 'Created': Created, 'Date & Time': Date_n_Time }

@App.route('/tags')
def Tags():
    URL = request.args.get('url')
    if not URL or 'https://toyhou.se/' not in URL:
        return Characters_URL
    
    Character = Request.get(URL).text
    Toyhouse = BeautifulSoup(Character, 'lxml')

    Tags = []

    Character_Tags = Toyhouse.find('div', 'profile-tags-content')
    for Tag in Character_Tags:
        Tag = Tag.text
        if Tag != '\n':
            Tags.append(Tag)

    return { 'Tags': Tags }

App.run(host="0.0.0.0", port='5656')