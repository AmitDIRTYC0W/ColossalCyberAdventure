from colossalcyberadventure.game import ColossalCyberAdventure


def main():
    game = ColossalCyberAdventure(700, 700, "coins")
    game.setup()
    game.run()


if __name__ == '__main__':
    main()
