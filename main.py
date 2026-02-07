import sys
import time

import os
from dotenv import load_dotenv

from schedule import every, repeat, run_pending

import logging
logger = logging.getLogger("LangaraCourseWatcherScraper") 
logger.setLevel(logging.INFO)

screen_handler = logging.StreamHandler()
formatter = logging.Formatter(fmt='[%(asctime)s] : [%(levelname)-8s] : %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
screen_handler.setFormatter(formatter)
logger.addHandler(screen_handler)
# logger.propagate = False


from Controller import Controller
load_dotenv()



DB_LOCATION="database/database.db"
CACHE_DB_LOCATION="database/cache/cache.db"
PREBUILTS_DIRECTORY="database/prebuilts/"
ARCHIVES_DIRECTORY="database/archives/"

   
@repeat(every(60).minutes)
def hourly(use_cache: bool = False):
    c = Controller()
    c.updateLatestSemester(False)
    c.setMetadata("last_updated")


@repeat(every(24).hours)
def daily(use_cache: bool = False):
    c = Controller()
    
    # check for next semester
    s = c.checkIfNextSemesterExistsAndUpdate()
    if s:
        logger.info(f"New semester detected.")
    else:
        logger.info("No new semester detected.")
    
    c.buildDatabase(use_cache)
    c.setMetadata("last_updated")
    
    



if __name__ == "__main__":
    logger.info("Launching Langara Course Watcher")
    
    if not os.path.exists("database/"):
        os.mkdir("database")
        
    # if not os.path.exists("database/cache"):
    #     os.mkdir("database/cache")

    if not os.path.exists(PREBUILTS_DIRECTORY):
        os.mkdir(PREBUILTS_DIRECTORY)

    # if not os.path.exists(ARCHIVES_DIRECTORY):
    #     os.mkdir(ARCHIVES_DIRECTORY)

    db_exists = os.path.exists(DB_LOCATION)

    controller = Controller()
    controller.create_db_and_tables()

    if db_exists:
        logger.info("Database found.")
        # controller.buildDatabase(use_cache=True)
    else:
        logger.info("Database not found. Building database from scratch.")
        controller.buildDatabase(use_cache=False)
        controller.setMetadata("last_updated")

    logger.info("Initialization complete.")
    
    daily(use_cache=False)
    hourly(use_cache=False)

    while True:
        run_pending()
        time.sleep(1)