from webscraper.process import start


def discord_start(*args):
    manager = ProcessManager()
    return manager


if __name__ == "__main__":
    start(products=["Maito"], stores=["Prisma Olari", "S-Market Grani", "Prisma Sello"], limit=5)

#TODO
#Pageclasses refactoring
#Datamanager refactoring
#Data export in webber.py refactoring