from Firebase import db, auth
from Character import Character
from Player import Player


def get_user(user_id):
    return db.child('users').child(user_id).get().val()


def login(email, password):
    data = auth.sign_in_with_email_and_password(email, password)
    user_id = data['localId']
    user = get_user(user_id)
    print(user)
    return Player(player_data=user)


def signup(email, password):
    data = auth.create_user_with_email_and_password(email, password)
    user_id = data['localId']
    user_nickname = email.split('@')[0]
    user_character = Character().json()
    user = {
        'id': user_id,
        'email': email,
        'nickname': user_nickname,
        'isActive': False,
        'isAttacked': False,
        'hasJoined': False,
        'character': user_character
    }
    db.child('users').child(user_id).set(user)
    return Player(player_data=user)
