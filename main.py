# Toyhou.se - API | Python ~ 10/12/21; October 12, 2021

"""
Started on: 10/12/21; October 12, 2021
Finished on: 10/18/21; October 18, 2021
"""

from flask import Flask, request, render_template
import requests as Request
from bs4 import BeautifulSoup

App = Flask(
    'app', template_folder='Template',
    static_url_path='/Template', static_folder='Template'
)

App.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

Title = 'Toyhou.se | API'
Description = 'Tired from copy and pasting characters\' information? Well i got ya, an API for Toyhou.se'

Characters_URL = { 'message': 'You have to provide a character\'s url.' }
User_Message = { 'message': 'You have to provide a username.' }
Page_Message = { 'message': 'Page has to be a number.' }

@App.route('/')
def Toyhouse():
    # return {
    #     'Toyhou.se': [
    #         '/creator?url='
    #     ]
    # }

    return render_template(
        'index.html', Title=Title,
        Description=Description,
        Routes=[
            'Creator', 'Character',
            'Profile', 'Gallery',
            'Creation', 'Tags',
            'All', 'Stats',
            'Characters', 'Arts',
            'Favorites',
            'Registration', 'Worlds',
            'Literatures',
            'Username_Log', 'Links'
        ]
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

# Stats ~ 11/11/21; November 11, 2021

@App.route('/stats')
def Stats():
    User = request.args.get('username')
    if not User: return User_Message
    
    Stats = Request.get(f"https://toyhou.se/{User}/stats").text
    if 'We can\'t find that page!' in Stats:
        return User_Message

    Toyhouse = BeautifulSoup(Stats, 'lxml')

    User = Toyhouse.find('span', 'display-user')
    # print(User)
    
    Username = User.a.text
    Avatar = User.img['src']

    User_Stats = Toyhouse.find('div', 'stats-content').findAll('dl')
    # print(User_Stats)

    Values = []
    for Row in User_Stats:
        Fields = Row.findAll('dd')
        for Field in Fields:
            Value = [Character for Character in Field.text]
            Value = list(
                filter(lambda Character: Character != '\n', Value)
            )

            Values.append(''.join(Value))

    # print(Values)

    return {
        'Username': Username, 'Avatar': Avatar,
        'Time_Registered': Values[0],
        'Last_Logged_In': Values[1],
        'Invited_By': Values[2],
        'Characters': Values[3],
        'Images': Values[4],
        'Literatures': Values[5],
        'Words': Values[6],
        'Forum_Posts': Values[7],
        'Subscribed_To': Values[8],
        'Subscribed_To_By': Values[9],
        'Authorizing': Values[10],
        'Authorized_By': Values[11]
    }

# Characters & Arts ~ 11/12/21; November 12, 2021

@App.route('/characters')
def Characters():
    User = request.args.get('username')
    Page = request.args.get('page') or 1
    Return = request.args.get('return') or ''
    
    if not User: return User_Message

    try:
        Page = int(Page)
    except:
        return Page_Message

    Return = Return.lower()

    # return { 'Page': Page, 'Return': Return }

    Characters = Request.get(
        f"https://toyhou.se/{User}/characters/folder:all?page={Page}"
    ).text
    if 'Invalid user selected.' in Characters:
        return User_Message

    Toyhouse = BeautifulSoup(Characters, 'lxml')
    Characters = []

    Users_Characters = Toyhouse.find('div', 'characters-gallery')
    Characters_Row = Users_Characters.find('div', 'gallery-row')
    Characters_List = Characters_Row.findAll('div', 'gallery-item')

    for Character in Characters_List:
        # print(Character)
        # break

        Name = Character.find(
            'div', 'thumb-caption'
        ).find('span', 'thumb-character-name').text
        Avatar = Character.find(
            'div', 'thumb-image'
        ).a.img['src']

        # if not Name and not Avatar: return
        if 'name' in Return: Characters.append(Name)
        elif 'avatar' in Return: Characters.append(Avatar)
        else:
            Characters.append({ 'Name': Name, Avatar: Avatar })

    return { 'Characters': Characters }

@App.route('/arts')
def Arts():
    User = request.args.get('username')
    Page = request.args.get('page') or 1

    if not User: return User_Message

    try:
        Page = int(Page)
    except:
        return Page_Message

    Arts = Request.get(
        f"https://toyhou.se/{User}/art?page={Page}"
    ).text
    if 'Invalid user selected.' in Arts:
        return User_Message

    Toyhouse = BeautifulSoup(Arts, 'lxml')
    Arts = []

    Gallery = Toyhouse.findAll('li', 'gallery-item')
    for Art in Gallery:
        Art = Art.find('div', 'gallery-thumb').a['href']
        Arts.append(Art)

    return { 'Arts': Arts }

# Favorites & Registration ~ 12/7/21; December 7, 2021

@App.route('/favorites')
def Favorites():
    User = request.args.get('username')
    Page = request.args.get('page') or 1

    if not User: return User_Message

    try:
        Page = int(Page)
    except:
        return Page_Message

    Favorites = Request.get(
        f"https://toyhou.se/{User}/favorites?page={Page}"
    ).text
    if 'Invalid user selected.' in Favorites:
        return User_Message

    Toyhouse = BeautifulSoup(Favorites, 'lxml')
    Favorites = []

    Characters = Toyhouse.findAll('div', 'gallery-item')
    for Character in Characters:
        Name = Character.find('div', 'thumb-caption').span.text
        Avatar = Character.find('div', 'thumb-image').a.img['src']
        Favorites.append({ 'Name': Name, 'Avatar': Avatar })
    
    return { 'Favorites': Favorites }

@App.route('/registration')
def Registration():
    User = request.args.get('username')
    if not User: return User_Message

    Stats = Request.get(f"https://toyhou.se/{User}/stats").text
    if 'Invalid user selected.' in Stats:
        return User_Message

    Toyhouse = BeautifulSoup(Stats, 'lxml')

    Stats = Toyhouse.find('div', 'stats-content').dl
    Time_Registered = Stats.find('dd', 'field-value')
    Registration = Time_Registered.text[1:-1]

    return Registration



App.run(host='0.0.0.0', port='5656')