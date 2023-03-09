import asyncio

from src.colossalcyberadventure.colossal_cyber_adventure import ColossalCyberAdventure


async def main():
    game = ColossalCyberAdventure()
    game.setup()
    game.run()


if __name__ == '__main__':
    asyncio.run(main())
