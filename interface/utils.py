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
    return json.dumps(data)

if __name__ == '__main__':
    print google_place_details('ChIJN1t_tDeuEmsRUsoyG83frY4')
