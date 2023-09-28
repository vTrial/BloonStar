import bs_fns
import requests

def create():
	conn = bs_fns.db_conn()
	with conn:
		with conn.cursor() as cur:
			cur.execute((
				"create table if not exists users("
					"id text primary key, "
					"name text"
				")"
			))
	conn.close()

def fill():
	# change season every season
	season = bs_fns.current_season()
	print("filling users db")
	lb_total_pages = bs_fns.lb_total_pages(season)
	
	conn = bs_fns.db_conn()
	with conn:
		with conn.cursor() as cur:
			for lb_page_num in range(1, lb_total_pages + 1):
				lb_url = f"https://data.ninjakiwi.com/battles2/homs/season_{str(season - 1)}/leaderboard?page={lb_page_num}"
				lb_json = requests.request("GET", lb_url).json()
				if lb_json["success"]:
					for user in lb_json["body"]:
						user_id = bs_fns.profile_url_to_id(user["profile"])
						insert_query = (
							"insert into users (id, name) "
							"values (%s, %s) "
							"on conflict (id) "
							"do update set name = excluded.name;"
						)
						insert_vals = (user_id, user['displayName'])
						cur.execute(insert_query, insert_vals)
	conn.close()
