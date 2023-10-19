import { supabase } from "$lib/supabaseClient"
import nDaysAgo from "$lib/bsFns"
import { heroNames } from "$lib/ThingAliases"

export const GET = async ({ url }) => {
  const daysAgo = 7
  const heroes = Object.keys(heroNames)
  const map_name = url.searchParams.get("map") ?? ""
  // Define hero_counts object to store hero data
  const hero_counts = {}

  const heroPromises = heroes.map(async (hero) => {
    const { data, error } = await supabase.rpc("hero_totals", {
      hero: hero,
      map_name: map_name,
      time_cutoff: nDaysAgo(daysAgo),
    })
    hero_counts[hero] = data[0]
  })

  await Promise.all(heroPromises)
  return new Response(JSON.stringify(hero_counts))
}
