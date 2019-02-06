from flask import Flask
from flask_restful import reqparse, Resource, Api
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)

PICKUPS = []
url = 'https://twitter.com/pickupIines'

try:
    with closing(get(url, stream=True)) as resp:
        content_type = resp.headers['Content-Type'].lower()
        if (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1):
            html = BeautifulSoup(resp.content, 'html.parser')
            for p in html.select('p.tweet-text'):
                line = p.text.replace('\n',' ')
                print(line)
                PICKUPS.append(line)
except RequestException as e:
    print('Error during requests to {0} : {1}'.format(url, str(e)))

parser = reqparse.RequestParser()
parser.add_argument('line')

class TestApi(Resource):
    def get(self):
        return "hello world!"

class PickupList(Resource):
    def get(self):
        return {'pickups': PICKUPS}

class Pickup(Resource):
    def get(self, pickup_id):
        return PICKUPS[pickup_id]

api.add_resource(TestApi, '/')

api.add_resource(PickupList, '/pickup')

api.add_resource(Pickup, '/pickup/<int:pickup_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
