from BaseStats import BASE_STATS
from Firebase import db
from random import randint


class Character:
    def __init__(self, character_data=BASE_STATS, player=None):
        self.player = player
        self.level = character_data['level']
        self.experience = character_data['experience']
        self.max_hp = character_data['maxHp']
        self.hp = self.max_hp

    def attack(self, enemy):
        attack = randint(0, 20)
        print(f"Player {self.player.nickname} attacks {enemy.nickname} for {attack} dmg")
        return attack

    def rs(self):
        self.hp = self.max_hp
        if self.experience >= 100 * self.level:
            self.experience -= 100 * self.level
            self.level += 1
            self.max_hp += 10
        db.child('users').child(self.player.id).child('character').update(self.json())

    @property
    def is_alive(self):
        return self.hp > 0

    def json(self):
        return {
            'level': self.level,
            'experience': self.experience,
            'maxHp': self.hp
        }

    def __str__(self):
        return f"""
                PLAYER: {self.player.nickname}
                LEVEL: {self.level}
                EXPERIENCE: {self.experience}
                HP: {self.max_hp}
        """
