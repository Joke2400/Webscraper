from pathlib import Path

class WorkingDirFilePath:
    path = Path.cwd()

class UserHomePath:
    path = Path.home()

class FoodieWebscraperPath:
    scraper_path = r"C:\Users\Joke\Desktop\Webscraper(completed spider)"
    #This path is going to be hardcoded for now, remember to change if file is moved.

class FilePaths:
    stores_path = WorkingDirFilePath.path / "webscraper" / "foodie_webscraper" / "spiders" / "foodie_package" / "stores.json"
    response_path = WorkingDirFilePath.path / "webscraper" / "foodie_webscraper" / "spiders" / "foodie_package" / "response.html"
    log_path = WorkingDirFilePath.path / "log.txt"
    #These will also have to be changed later to more robust paths...

#print(Path(__file__).parent.resolve()) #magic line to be used later