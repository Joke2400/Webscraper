from pathlib import Path

class WorkingDirFilePath:
    path = Path.cwd()

class UserHomePath:
    path = Path.home()

class WebscraperPath:
    path = Path(r"C:\Users\Joke\Desktop\Webscraper")
    #This path is going to be hardcoded for now, remember to change if file is moved.

class GMapsAPIKeyPath:
    keypath = r"C:\Users\Joke\Desktop\google_cloud_api.txt"

class FilePaths:
    stores_path = WebscraperPath.path / "webscraper" / "data" / "stores.json"
    response_path = WebscraperPath.path / "webscraper" / "data" / "response.html"
    database_path = WebscraperPath.path / "webscraper" / "data" / "database.db"
    log_path = WebscraperPath.path / "log.txt"
    settings_path = 'webscraper.webscraper_package.settings' 

    #print(Path(__file__).parent.resolve()) #I've no clue why i put this here but it must be important then