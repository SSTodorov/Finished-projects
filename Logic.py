"""This is the logic for the main file. """
import requests


def get_weather(city):
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={},uk'
                                    '&appid=a6a0bbb438d0c47d26e1e3b60d1b6041'.format(city))
    json_weather = r.json()
    return json_weather


def get_news(city):
    link = 'https://newsapi.org/v2/everything?'
    api_key = 'c466e4b6474b46e9a30b6d385188fe19'
    parameters = {
        'q': city,
        'pageSize': 100,
        'apiKey': api_key
    }
    r = requests.get(link, params=parameters)
    r_json = r.json()
    return r_json


def get_headlines(json_object):
    headlines = []
    for i in json_object['articles']:
        headlines.append(i['title'])
    return headlines


def get_article_link(json_object, title):
    for i in json_object['articles']:
        if i['title'] == title:
            return i['url']


def get_transport_info(city_start, city_end, travel_date):
    app_id = '205d70d1'
    app_key = 'acb6b8abdf9ea7604752d1207c624841'
    parameters = {
        'nationalSearch': 'true',
        'date': travel_date,
        'app_id': app_id,
        'app_key': app_key,
    }

    r = requests.get('https://api.tfl.gov.uk/journey/journeyresults/{}/to/{}'.format(city_start, city_end),
                     params=parameters)
    r_json = r.json()
    start_location = []
    start_location_time = []
    end_location = []
    end_location_time = []
    trip_duration = []

    if r.status_code == 200:
        journeys_raw = r_json['journeys']

        for journey_idx, journey in enumerate(journeys_raw):
            legs = journey['legs']

            for leg_idx, leg in enumerate(legs):
                arrival = leg['arrivalPoint']
                departure = leg['departurePoint']
                start_location.append(departure['commonName'])
                start_location_time.append(leg['departureTime'])
                end_location.append(arrival['commonName'])
                end_location_time.append(leg['arrivalTime'])

        full_data = {
            'departurePoint': start_location,
            'departureTime': start_location_time,
            'arrivalPoint': end_location,
            'arrivalTime': end_location_time,
            'duration': trip_duration
        }
        return full_data

    else:
        print('The programmer ran out of time!')

# get_transport_info('Liverpool Street Underground Station', 'Eastleigh (Hants), Southampton Airport, Parkway Station', '20190503')
