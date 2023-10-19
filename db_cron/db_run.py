import schedule
import time
import asyncio

import bs_fns
import matches_db
import users_db
import hom_users_db

def update_databases():
	users_db.fill()
	hom_users_db.fill()
	asyncio.run(matches_db.fill())

def main():
    # Update db on boot
    # then schedule the task to run every 60 minutes
    update_databases()
    schedule.every(60).minutes.do(update_databases)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()