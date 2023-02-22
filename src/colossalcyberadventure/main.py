from colossal_cyber_adventure import ColossalCyberAdventure
import glob


def main():
    print(glob.glob("./*"))
    game = ColossalCyberAdventure()
    game.setup()
    game.run()


if __name__ == '__main__':
    main()
