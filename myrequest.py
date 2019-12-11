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
                       {'name': 'lee', 'hobby': 'basketball'}).json())
    print(send_request('sign-up',
                       {'name': 'kim', 'hobby': 'soccer'}).json())
    print(send_request('sign-up',
                       {'name': 'park', 'hobby': 'watching movie'}).json())
    print(send_request('tweet',
                        {'id': 0, 'tweet': 'i`m tired.'}).json())
    print(send_request('tweet',
                        {'id': 2, 'tweet': 'i`m happy.'}).json())
    print(send_request('tweet',
                       {'id': 1, 'tweet': 'i`m hungry.'}).json())
    print(send_request('tweet',
                       {'id': 1, 'tweet': 'i`m thirsty.'}).json())
    print(send_request('follow',
                       {'id': 0, 'follow': 1}).ok)
    print(send_request('follow',
                       {'id': 1, 'follow': 0}).ok)
    print(send_request('unfollow',
                       {'id': 1, 'follow': 0}).ok)
    print(send_request('follow',
                       {'id': 0, 'follow': 2}).ok)
    print(send_request('timeline/%s' % 0, {}, 'GET').json())
