from flask import Flask, jsonify, request, current_app
from sqlalchemy import create_engine, text


def is_user(user_id):
    for user in current_app.users:
        if user['id'] == user_id:
            return True
    return False


def insert_user(user):
    return current_app.db.execute(text("""
            INSERT INTO users (
                user_name,
                email,
                myprofile,
                hashed_password
            ) VALUES (
                :user_name,
                :email,
                :myprofile,
                :hashed_password
            )
        """), user)


def insert_tweet(message):
    return current_app.db.execute(text(
        """
        insert into tweets (
            user_id,
            tweet
        ) values (
            :user_id,
            :tweet
        )
        """
    ), message)


def get_follow(follow):
    cursor = current_app.db.execute(text(
        """
        select isfollowing
        from users_following
        where user_id = :user_id and
              user_id_following = :user_id_following
        """
    ), follow)
    res = cursor.fetchone()
    if res:
        return {'isfollowing': 1-res[0]}
    return {}


def upsort_follow(follow):
    isfollowing = get_follow(follow)
    follow.update(isfollowing)
    return current_app.db.execute(text(
        """
        insert into users_following (
        user_id,
        user_id_following
        ) values (
        :user_id,
        :user_id_following
        )
        on duplicate key update isfollowing = :isfollowing 
        """
    ), follow)


def run_app(config=None):
    app = Flask(__name__)
    if config is None:
        app.config.from_json('test_config.json')
    else:
        app.config.update(config)
    app.db = create_engine(app.config['DB_URL'], encoding='utf-8')

    @app.route('/check', methods=['GET'])
    def check():
        return '', 202

    @app.route('/sign-up', methods=['POST'])
    def sign_up():
        new_user = request.json
        insert_user(new_user)
        return jsonify(new_user)

    @app.route('/tweet', methods=['POST'])
    def tweet():
        """
        less then 300 chars
        """
        message = request.json
        if len(message.get('tweet', '')) > 300:
            return 'Exceed 300 chars', 400
        insert_tweet(message)
        return jsonify(message)

    @app.route('/follow', methods=['POST'])
    def follow():
        data = request.json
        upsort_follow(data)
        return '', 202

    @app.route('/timeline/<int:user_id>', methods=['GET'])
    def timeline(user_id):
        cursor = current_app.db.execute(text(
            """
            select _id, tweet
            from tweets
            where user_id = :user_id
            """
        ), {'user_id': int(user_id)})
        tweets = cursor.fetchall()
        return dict(tweets)

    return app


if __name__ == '__main__':
    run_app().run(debug=True)