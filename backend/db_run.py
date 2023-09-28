import schedule
import time

import bs_fns
import matches_db
import users_db
import hom_users_db

def update_databases():
	# Create and/or fill players database table
	users_db.create()
	users_db.fill()
	print("created users")
	# Create and/or fill players database table
	hom_users_db.create()
	hom_users_db.fill()
	print("created hom users")
	# Create and/or fill matches database table
	matches_db.create()
	matches_db.fill()
	print("created matches")

# Schedule the task to run every 60 minutes
update_databases()

schedule.every(60).minutes.do(update_databases)
while True:
	schedule.run_pending()
	time.sleep(1)

