import time

import schedule

from service import FrogJiraMain

schedule.every().day.at("12:00").do(FrogJiraMain.jiraMain)
schedule.every().day.at("18:00").do(FrogJiraMain.jiraMain)
schedule.every().day.at("00:00").do(FrogJiraMain.jiraMain)
while True:
    schedule.run_pending()
    time.sleep(2)
