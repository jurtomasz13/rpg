from Game import Game


def main():
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        print("### Game forcefully closed! ###")
    except EOFError:
        print("### Game forcefully closed! ###")
    finally:
        game.player.set_offline()


if __name__ == '__main__':
    main()
