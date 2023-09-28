import requests
import db_fns

# create users db if doesn't exist
def createHomUsersDb():
	conn = db_fns.get_database_connection()
	with conn:
		with conn.cursor() as cur:
			cur.execute((
				"create table if not exists hom_users("
					"season integer, "
					"user_id text, "
					"score integer, "
					"primary key (season, user_id),"
					"foreign key (user_id) references users(id)"
				")"
			))
	conn.close()


def fillHomUsersDb():
	# change season every season
	conn = db_fns.get_database_connection()
	season = 14
	print("filling hom users db")
	lb_total_pages = db_fns.get_lb_total_pages(season)
	with conn:
		with conn.cursor() as cur:
			for lb_page_num in range(1, lb_total_pages + 1):
				lb_url = f"https://data.ninjakiwi.com/battles2/homs/season_{str(season - 1)}/leaderboard?page={lb_page_num}"
				lb_json = requests.request("GET", lb_url).json()
				if lb_json["success"]:
					for user in lb_json["body"]:
						user_id = db_fns.profile_url_to_id(user["profile"])
						insert_query = (
							"insert into hom_users (season, user_id, score) "
							"values (%s, %s, %s)"
							"on conflict (season, user_id) "
							"do update set score = excluded.score;"
						)
						insert_vals = (season, user_id, user["score"])
						cur.execute(insert_query, insert_vals)
	conn.close()