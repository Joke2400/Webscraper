from webscraper.process import start


def discord_start(*args):
    manager = ProcessManager()
    return manager


if __name__ == "__main__":
    start(products=[
        "Jauheliha",
        "Tofukuutio",
        "Margariini",
        "Rasvaton Maito",
        "Kermajuusto",
        "Ruokakerma",
        "Ruisleipä",
        "Broilerileike",
        "Appelsiinimehu"
        "Spagetti",
        "Riisi",
        "Tomaattimurska",
        "Ketsuppi",
        "Kahvi",
        "Coca Cola",
        "Tomaatti",
        "Kurkku",
        "Peruna",
        "Porkkana",
        "Sipuli",
        "Kukkakaali",
        "Paprika",
        "Jääsalaatti",
        "Basilika",
        "Banaani",
        "Appelsiini",
        "Omena",
        "Klementiini",
        "Vihreä Rypäle"], 
    stores=["Prisma Järvenpää", "S-Market Karjaa", "Prisma Olari", "Prisma Sello", "S-Market Grani"],
    limit=25,
    reset=False)

    #TODO
    #Pageclasses refactori5ng
    #Datamanager refactoring
    #Data export in webber.py refactoring
    