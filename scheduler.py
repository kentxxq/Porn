# coding:utf-8


import schedule
import subprocess
import time
import os


def incremental_crawl():
    subprocess.Popen('scrapy crawlall -i', cwd=os.getcwd(),
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


schedule.every().days.at('12:12').do(incremental_crawl)


while True:
    schedule.run_pending()
    time.sleep(1)
