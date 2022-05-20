from Firebase import db


class Duel:
    def __init__(self, player_id):
        self.id = player_id
        self.move = 1
        self.moves = {
            'move': self.move,
            'moves': {}
        }
        self.remove()
        db.child('fights').child(self.id).update(self.moves)

    def update(self):
        self.move = db.child('fights').child(self.id).get().val()['move']
        self.moves = db.child('fights').child(self.id).get().val()['moves']

    def remove(self):
        db.child('fights').child(self.id).remove()

    def attack(self, dmg):
        self.moves['moves'][self.move] = {'attack': dmg}

    def dodge(self):
        self.moves['moves'][self.move] = {'dodge': True}

    def dodge_failed(self):
        self.moves['moves'][self.move] = {'dodge': False}

    def run(self):
        self.moves['moves'][self.move] = {'run': True}

    def run_failed(self):
        self.moves['moves'][self.move] = {'run': False}

    @property
    def last_move(self):
        try:
            moves = list(self.moves['moves'].items())[-1]
            key, value = moves
            last_move = {f'{key}': value}
        except AttributeError:
            last_move = None
        except IndexError:
            last_move = None
        return last_move

    @property
    def penultimate(self):
        try:
            penultimate = self.moves['moves'][self.moves['moves'].keys()[-2]]
        except AttributeError:
            penultimate = None
        return penultimate

    @property
    def exists(self):
        if db.child('fights').child(self.id).get().val() is not None:
            return True
        else:
            return False

    @property
    def round(self):
        return
