import bs_fns
import requests


def fill():
	supabase = bs_fns.supabase_auth()
	# change season every season
	season = bs_fns.current_season()
	lb_total_pages = bs_fns.lb_total_pages(season)
	# accumulate things to upsert here
	users_lst = []
	# for each page in a season
	for lb_page_num in range(1, lb_total_pages + 1):
		lb_url = f"https://data.ninjakiwi.com/battles2/homs/season_{str(season - 1)}/leaderboard?page={lb_page_num}"
		lb_json = requests.request("GET", lb_url).json()
		if lb_json["success"]:
			# for each player in page
			for user in lb_json["body"]:
				user_id = bs_fns.profile_url_to_id(user["profile"])
				users_lst += [{'id': user_id, 'name': user['displayName']}]
	supabase.table('users') \
		.upsert(users_lst) \
		.execute()