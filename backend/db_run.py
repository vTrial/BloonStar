import schedule
import time

import db_fns
import matches_db
import users_db
import hom_users_db

def update_databases():
	# Create and/or fill players database table
	users_db.createUsersDb()
	users_db.fillUsersDb()
	print("created users")
	# Create and/or fill players database table
	hom_users_db.createHomUsersDb()
	hom_users_db.fillHomUsersDb()
	print("created hom users")
	# Create and/or fill matches database table
	matches_db.createMatchesDb()
	matches_db.fillMatchesDb()
	print("created matches")

# Schedule the task to run every 60 minutes
update_databases()

schedule.every(60).minutes.do(update_databases)
while True:
	schedule.run_pending()
	time.sleep(1)

