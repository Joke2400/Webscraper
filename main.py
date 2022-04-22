from webscraper.process import start


def discord_start(*args):
    manager = ProcessManager()
    return manager


if __name__ == "__main__":
    start(products=["Pasta", "Kana", "Riisi", "Sandels"], stores=["Prisma Olari", "S-market Grani", "Prisma Sello"], limit=5)

#TODO
#Pageclasses refactori5ng
#Datamanager refactoring
#Data export in webber.py refactoring5