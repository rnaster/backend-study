from flask import Flask, jsonify, request

app = Flask(__name__)
app.users = []
app.user_id_cnt = 0
app.tweets = []
app.tweets_id_cnt = 0
app.follow = {}


@app.route('/check', methods=['GET'])
def check():
    return '', 202


@app.route('/sign-up', methods=['POST'])
def sign_up():
    new_user = request.json
    new_user['id'] = app.user_id_cnt
    app.users.append(new_user)
    app.user_id_cnt += 1
    return jsonify(new_user)


def is_user(user_id):
    for user in app.users:
        if user['id'] == user_id:
            return True
    return False


@app.route('/tweet', methods=['POST'])
def tweet():
    """
    less then 300 chars
    """
    data = request.json
    user_id = int(data.get('id', -1))
    text = data.get('tweet', '')
    if not is_user(user_id):
        return 'Wrong user id', 400
    if len(text) > 300:
        return 'Exceed 300 chars', 400
    app.tweets.append({
        '_id': app.tweets_id_cnt,
        'user_id': user_id,
        'tweet': text
    })
    app.tweets_id_cnt += 1
    return jsonify(app.tweets[-1])


@app.route('/follow', methods=['POST'])
def follow():
    data = request.json
    source = int(data.get('id', 0))
    target = int(data.get('follow', 0))
    if not is_user(source) or not is_user(target):
        return 'Wrong user id', 400
    app.follow.setdefault(source, {target}).add(target)
    print(app.follow)
    return '', 202


@app.route('/unfollow', methods=['POST'])
def unfollow():
    data = request.json
    source = int(data.get('id', 0))
    target = int(data.get('follow', 0))
    if not is_user(source) \
            or not is_user(target) \
            or target not in app.follow.get(source, set()):
        return 'Wrong user id', 400
    app.follow[source].remove(target)
    print(app.follow)
    return '', 202


@app.route('/timeline/<int:user_id>', methods=['GET'])
def timeline(user_id):
    my_timeline = []
    for f_user in app.follow.get(user_id, set()):
        last_tweet = {'user_id': f_user, 'tweet': ''}
        for tweet in app.tweets:
            if tweet['user_id'] == f_user:
                last_tweet = tweet
        my_timeline.append(last_tweet)
    return jsonify(my_timeline)


if __name__ == '__main__':
    app.run()