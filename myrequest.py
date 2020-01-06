import json
import requests

url = 'http://localhost:5000'
headers = {'Content-Type': 'application/json; charset=utf-8'}


def send_request(endpoint, body, methods='POST'):
    if methods == 'GET':
        return requests.get('%s/%s' % (url, endpoint))
    body = json.dumps(body)
    return requests.post('%s/%s' % (url, endpoint),
                         data=body,
                         headers=headers)


if __name__ == "__main__":
    print(send_request('check', {}, 'GET').ok)
    print(send_request('sign-up',
                       {'user_name': 'lee',
                        'myprofile': 'i like League of Legend',
                        'email': 'lee@never.com',
                        'hashed_password': 'lol'}).json())
    print(send_request('sign-up',
                       {'user_name': 'kim',
                        'myprofile': 'i`m studying Flask in Python. it`s very boring',
                        'email': 'kim@never.com',
                        'hashed_password': 'what'}).json())
    print(send_request('sign-up',
                       {'user_name': 'park',
                        'myprofile': 'i love basketball',
                        'email': 'park@never.com',
                        'hashed_password': 'ball'}).json())
    print(send_request('tweet',
                        {'user_id': 1, 'tweet': 'i`m tired.2'}).content)
    print(send_request('tweet',
                        {'user_id': 2, 'tweet': 'i`m happy.2'}).text)
    print(send_request('tweet',
                       {'user_id': 3, 'tweet': 'i`m hungry.2'}).status_code)
    print(send_request('tweet',
                       {'user_id': 2, 'tweet': 'i`m thirsty.2'}))
    print(send_request('follow',
                       {'user_id': 1, 'user_id_following': 2}))
    print(send_request('follow',
                       {'user_id': 1, 'user_id_following': 4}))
    print(send_request('timeline/2', {}, 'GET').json())
