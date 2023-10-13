import requests
import time
import pandas as pd
import asyncio
from aiolimiter import AsyncLimiter
import httpx
import bs_fns

limiter = AsyncLimiter(max_rate=100, time_period=60)

async def fetch_and_process_match(user_id, supabase, season, user_count):
    player_matches = []
    time_of_match = int(time.time())
    user_matches_url = f"https://data.ninjakiwi.com/battles2/users/{user_id}/matches"
    async with httpx.AsyncClient() as client:
        # ensure not over api limits
        async with limiter:
        # Perform a request
            response = await client.get(user_matches_url, timeout=60 + user_count * 0.6)
        user_matches_json = response.json()
    # check if endpoint works
    if user_matches_json["success"]:
        for user_match in user_matches_json["body"]:
            left_side = user_match["playerLeft"]
            right_side = user_match["playerRight"]
            left_id = bs_fns.profile_url_to_id(left_side["profileURL"])
            right_id = bs_fns.profile_url_to_id(right_side["profileURL"])
            left_tower_1, left_tower_2, left_tower_3 = sorted([left_side["towerone"], left_side["towertwo"], left_side["towerthree"]])
            right_tower_1, right_tower_2, right_tower_3 = sorted([right_side["towerone"], right_side["towertwo"], right_side["towerthree"]])

            player_matches.append({
                'id': user_match["id"],
                'left_id': left_id,
                'right_id': right_id,
                'map': user_match['map'],
                'gametype': user_match['gametype'],
                'left_hero': left_side["hero"],
                'left_tower_1': left_tower_1,
                'left_tower_2': left_tower_2,
                'left_tower_3': left_tower_3,
                'right_hero': right_side["hero"],
                'right_tower_1': right_tower_1,
                'right_tower_2': right_tower_2,
                'right_tower_3': right_tower_3,
                'left_outcome': left_side["result"],
                'duration': user_match["duration"],
                'end_round': user_match["endRound"],
                'time': time_of_match
            })
        return player_matches

async def fill():
    supabase = bs_fns.supabase_auth()
    season = bs_fns.current_season()
    data = supabase.table('hom_users') \
        .select('user_id') \
        .eq('season', season) \
        .execute().data
    # select has funny output; change to 1d list in the next line
    user_ids = [user['user_id'] for user in data]
    # accumulate things to upsert here
    matches_lst = []
    user_count = len(user_ids)
    tasks = []
    for user_id in user_ids:
        task = fetch_and_process_match(user_id, supabase, season, user_count)
        tasks.append(task)
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)
    for result in results:
        matches_lst.extend(result)
    # surely there's a faster way than turning to df and back
    matches_df = pd.DataFrame.from_dict(matches_lst)
    matches_df = matches_df.drop_duplicates(subset=['id'])
    matches_lst = matches_df.to_dict(orient='records')
    supabase.table('matches').upsert(matches_lst).execute()
