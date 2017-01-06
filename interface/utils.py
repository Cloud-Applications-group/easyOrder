import json
import requests
import urllib2

GOOGLE_API_KEY = 'AIzaSyBCinQHLTxOHgFXAFHjsftWjucn2cI3yWg'


def google_place_details(location_id):

    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = dict(
        placeid=location_id,
        key=GOOGLE_API_KEY
    )

    resp = requests.get(url=url, params=params)
    data = (json.loads(resp.text))
    r = requests.get('https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=' +
                     data['result']['photos'][0][
                         'photo_reference'] + '&key=AIzaSyBCinQHLTxOHgFXAFHjsftWjucn2cI3yWg')
    data['result']['photos'][0]['photo_reference'] = r.url
    if validate_google_data(data):
        return json.dumps(data)
    return False


def validate_google_data(data):

    if 'result' in data:
        validate_list = ['rating', 'photos', 'name', 'opening_hours', 'place_id']
        if all(name in data['result'] for name in validate_list):

            if not len(data['result']['photos']) > 0:
                return False

            photos_list = ['open_now', 'periods', 'weekday_text']
            if  not all(name in data['result']['opening_hours'] for name in photos_list):
                return False
            return True
        return False
    return False


if __name__ == '__main__':
    print google_place_details('ChIJN1t_tDeuEmsRUsoyG83frY4')
