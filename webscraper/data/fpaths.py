from pathlib import Path

class WorkingDirFilePath:
    path = Path.cwd()

class UserHomePath:
    path = Path.home()

class FoodieWebscraperPath:
    scraper_path = r"C:\Users\Joke\Desktop\Webscraper(completed spider)"
    #This path is going to be hardcoded for now, remember to change if file is moved.

class FilePaths:
    stores_path = WorkingDirFilePath.path / "webscraper" / "data" / "stores.json"
    response_path = WorkingDirFilePath.path / "webscraper" / "data" / "response.html"
    log_path = WorkingDirFilePath.path / "log.txt"
    settings_path = 'webscraper.webscraper_package.settings' 

    #print(Path(__file__).parent.resolve()) #I've no clue why i put this here but it must be important then