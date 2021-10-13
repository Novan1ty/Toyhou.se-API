from flask import Flask, request

App = Flask('app')

@App.route('/')
def Endpoints():
    return {
        'Endpoints': [
            '/creator?url='
        ]
    }

@App.route('/creator')
def Creator():
    url = request.args.get('url')
    if not url:
        return { 'message': 'You have to provide a character\'s url' }

    # return url

App.run(host="0.0.0.0", port='5656')