from multiprocessing import freeze_support
from src.colossalcyberadventure.colossal_cyber_adventure import ColossalCyberAdventure
from src.colossalcyberadventure.tilemap import init_loader


def main():
    # Start the tilemap loader process
    init_loader()

    # Start the game
    game = ColossalCyberAdventure()
    game.setup()
    game.run()


if __name__ == "__main__":
    # freeze_support() is needed for multiprocessing to work on Windows
    freeze_support()
    main()
