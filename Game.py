import time

from Firebase import db
from Authentication import login, signup
from Duel import Duel
from Player import Player


class Game:
    def __init__(self):
        self.player = None
        self.enemy = None
        self.duel = None

    def initialization(self):
        while True:
            try:
                print("""
                ### ACCOUNT ###
                    Do you want to login or signup?
                1. Login
                2. Signup
                """)

                selected_option = int(input())

                if selected_option != 1 and selected_option != 2:
                    print("There is no such option!")
                    continue

                email = input("Enter your email\n")
                password = input("Enter your password\n")
                confirmed_password = input("Confirm your password\n")

                if password != confirmed_password:
                    print("Passwords don't match!")
                    continue

                if selected_option == 1:
                    self.player = login(email, password)
                elif selected_option == 2:
                    self.player = signup(email, password)
                # TO BE DELETED IF EVERYTHING WORKS FINE
                self.player.set_offline()
                self.player.set_joined_false()
                self.player.set_attack_false()
                ########################################
            except ValueError:
                print("Wrong value inserted!")
                continue
            except Exception:
                print("Something went wrong!")
                continue
            return

    def menu(self):
        db_listener = db.child('users').child(self.player.id).stream(self.db_listener)
        second_db_listener = db.child('fights').child(self.player.id).stream(self.db_listener)
        while True:
            try:
                self.player.set_online()

                print("""
                ### GAME ###
                    Choose your option:
                0. EXIT
                1. Attack someone
                2. Check status
                3. Respond to a duel!
                """)

                selected_option = int(input())

                if selected_option == 1:
                    print("Choose your opponent or go back (0)!")

                    players = {}
                    index = 0

                    for player in db.child('users').get().each():
                        index += 1
                        if player.val()['nickname'] == self.player.nickname:
                            index -= 1
                            continue
                        players[index] = player.val()

                    for player in players.items():
                        index, player_data = player
                        print(f"{index}: {player_data['nickname']} (Level: {player_data['character']['level']})")

                    selected_opponent = int(input())

                    if selected_opponent == 0:
                        continue
                    else:
                        self.enemy = Player(players[selected_opponent])
                        if self.enemy.is_active:
                            self.duel_online(attacker=True)
                        else:
                            self.duel_offline()
                        continue

                elif selected_option == 2:
                    print(self.player.character)
                    continue

                elif selected_option == 3:
                    if self.player.is_attacked:
                        self.duel_online(attacker=False)
                    else:
                        print("You are not currently challenged!")
                    continue

                elif selected_option == 0:
                    print("### Game closed ###")
                    db_listener.close()
                    second_db_listener.close()
                    quit()
                else:
                    print("There is no such option!")
                    continue
            except ValueError:
                print("Wrong value inserted!")
                continue
            except EOFError:
                print("### Game forcefully closed! ###")
            return

    def run(self):
        self.initialization()
        self.menu()

    def duel_online(self, attacker):
        self.player.set_offline()

        if attacker:
            self.duel = Duel(self.player.id)
            self.enemy.set_attack_true(self.player.id)
            timer = 20
            while not self.enemy.has_joined and timer > 0:
                print(f"Waiting for opponent to join {timer}")
                time.sleep(5)
                timer -= 5
            if not self.enemy.has_joined:
                self.duel_offline()
                return
            # while self.duel.exists and self.player.character.is_alive and self.enemy.character.is_alive:
            #     while self.duel.move % 2 == 0:
            #         if self.duel.last_move is not None:
            #             if list(self.duel.last_move.keys())[0] == 'attack':
            #                 self.player.character.hp -= self.duel.last_move['attack']
            #             if list(self.duel.last_move.keys())[0] == 'dodge':
            #                 if self.duel.last_move['dodge']:
            #                     print("Your opponent dodged!")
            #                 else:
            #                     pass
            #
            #             if list(self.duel.last_move.keys())[0] == 'run':
            #                 print("Your opponent ran away!")
            #                 self.duel.remove()
            #                 break
            #             else:
            #                 print("Something went wrong!")
            #
            #         print(f"""
            #         Choose your action:
            #         1. Attack
            #         2. Dodge
            #         3. Run
            #         """)
            #
            #         selected_option = int(input())
            #
            #         if selected_option == 1:
            #             self.duel.attack(self.player.character.attack())
            #         if selected_option == 2:
            #             chance = randint(0, 10)
            #             if chance <= .5:
            #                 self.duel.dodge()
            #             else:
            #                 self.duel.dodge_failed()
            #                 print("You failed to dodge!")
            #         if selected_option == 3:
            #             chance = randint(0, 10)
            #             if chance <= .3:
            #                 self.duel.run()
            #             else:
            #                 self.duel.run_failed()
            #                 print("You failed to run!")
            #
            #         self.duel.move += 1
            #         self.duel.update()
            #
            #     print("Duel has ended!")
            #     break
            #
            # if self.player.character.is_alive:
            #     print("Congratulations! You have won and gained 20exp")
            #     self.player.character.experience += 20
            #     self.enemy.character.experience += 10
            # else:
            #     print("Your opponent has won! You gained 10exp")
            #     self.enemy.character.experience += 20
            #     self.player.character.experience += 10
            #
            # self.player.character.rs()
            # self.enemy.character.rs()
        #
        # if not attacker:
        #     self.enemy = Player(get_user(self.player.get_attacker_id()))
        #     self.duel = Duel(self.enemy.id)
        #     self.player.set_joined_true()
        #     while self.duel.exists:
        #         while self.duel.move % 2 != 0:
        #             if self.duel.last_move is not None:
        #                 pass
        #             time.sleep(1)

        self.enemy.set_attack_false()
        self.player.set_joined_false()

    def duel_offline(self):
        self.player.set_offline()
        index = True
        while self.player.character.is_alive and self.enemy.character.is_alive:
            if index:
                self.player.character.hp -= self.enemy.character.attack(self.player)
                index = False
            else:
                self.enemy.character.hp -= self.player.character.attack(self.enemy)
                index = True
        if self.player.character.is_alive:
            print("Congratulations! You have won and gained 20exp")
            self.player.character.experience += 20
            self.enemy.character.experience += 10
        else:
            print("Your opponent has won! You gained 10exp")
            self.enemy.character.experience += 20
            self.player.character.experience += 10

        self.player.character.rs()
        self.enemy.character.rs()

    def db_listener(self, msg):
        try:
            if msg['data']['isAttacked']:
                print("You have been challenged to a duel!")
        except:
            pass
        try:
            if msg['path'] == '/attacked':
                self.duel.update()
        except:
            pass
