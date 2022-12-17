from collosalcyberadventure.client.colossalcyberadventure import ColossalCyberAdventure


def main():
    game = ColossalCyberAdventure(500, 500, "test")
    game.setup()
    game.run()


if __name__ == '__main__':
    main()
