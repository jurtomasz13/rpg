moves = {
    'move': 1,
    'moves': {
        'attack': 1,
        'dodge': 2
    }
}

hehs = moves['moves'].items()
lista = list(hehs)
key, value = lista[-1]
dicti = dict({f'key': value})

print(dicti)
