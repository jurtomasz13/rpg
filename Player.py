from Character import Character
from Firebase import db


class Player:
    def __init__(self, player_data):
        self.id = player_data['id']
        self.email = player_data['email']
        self.nickname = player_data['nickname']
        try:
            self.character = Character(player_data['character'], self)
        except KeyError:
            self.character = Character(player=self)

    @property
    def is_active(self):
        return db.child('users').child(self.id).get().val()['isActive']

    @property
    def is_attacked(self):
        return db.child('users').child(self.id).get().val()['isAttacked']

    @property
    def has_joined(self):
        return db.child('users').child(self.id).get().val()['hasJoined']

    def get_attacker_id(self):
        try:
            return db.child('users').child(self.id).child('attack').get().val()['enemyId']
        except:
            return None

    def set_joined_true(self):
        db.child('users').child(self.id).update({'hasJoined': True})

    def set_joined_false(self):
        db.child('users').child(self.id).update({'hasJoined': False})

    def set_online(self):
        db.child('users').child(self.id).update({'isActive': True})

    def set_offline(self):
        db.child('users').child(self.id).update({'isActive': False})

    def set_attack_true(self, enemy_id):
        db.child('users').child(self.id).update({'isAttacked': True})
        db.child('users').child(self.id).child('attack').set({'enemyId': enemy_id})

    def set_attack_false(self):
        db.child('users').child(self.id).update({'isAttacked': False})
        db.child('users').child(self.id).child('attack').remove()

    def __str__(self):
        return f"""
            ID: {self.id}
            EMAIL: {self.email}
            NICKNAME: {self.nickname}
            IS_ATTACKED: {self.is_attacked}
            HAS_JOINED: {self.has_joined}
            CHARACTER: "
                {self.character}
            "
            """
