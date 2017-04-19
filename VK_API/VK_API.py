import requests
import _datetime
from datetime import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


def get_friends(user_id, fields):
    """ Returns a list of user IDs or detailed
    information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = '# put your access token here'
    user_id = user_id

    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields
    }

    query = "{domain}/friends.get?access_token={access_token}"
    query += "&user_id={user_id}&fields={fields}&v=5.53".format(**query_params)
    response = requests.get(query)
    num = 0
    friends = []
    for man in response.json()['response']['items']:
        try:
            bdate = response.json()['response']['items'][num]['bdate']
            points = 0
            year = ''
            for i in bdate:
                if points == 2:
                    year += i
                if i == '.':
                    points += 1
            if points > 1:
                friends.append(int(year))
        except KeyError:
            pass
        num += 1
    return friends


def age_predict(user_id):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    years = get_friends(user_id, 'bdate')
    sum = 0
    for year in years:
        sum += 2017 - year
    age = sum // len(years)
    return age


def count_dates_from_messages(messages):
    day = -1
    dates = []
    freq = []
    for message in messages:
        new_day = datetime.fromtimestamp(message['date']).strftime("%Y-%m-%d")
        if new_day != day:
            dates.append(new_day)
            day = new_day
            freq.append(1)
        else:
            freq[len(freq) - 1] += 1
    return dates, freq


def messages_get_history(user_id, offset=0, count=200):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = '# put your access token here'
    user_id = user_id
    count = 200
    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'count': count
    }
    query = "{domain}/messages.getHistory?access_token={access_token}&"
    query += "user_id={user_id}&count={count}&v=5.60".format(**query_params)
    response = requests.get(query)
    dates, freq = count_dates_from_messages(
        response.json()['response']['items'])
    return dates, freq


def graph(user_id):
    plotly.tools.set_credentials_file(
        username='# put your username here', api_key='# put your api_key here')
    dates, freq = messages_get_history(user_id)
    data = [go.Scatter(x=dates, y=freq)]
    py.iplot(data)
