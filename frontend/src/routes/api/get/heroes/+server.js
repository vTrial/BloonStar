import { supabase } from "$lib/supabaseClient"

export const GET = async ({ url }) => {
  const map_name = url.searchParams.get("map") ?? ""
  // Define hero_counts object to store hero data
  const hero_counts = {}
  const heroes = [
    "Quincy",
    "Quincy_Cyber",
    "Gwendolin",
    "Gwendolin_Science",
    "StrikerJones",
    "StrikerJones_Biker",
    "Obyn",
    "Obyn_Ocean",
    "Churchill",
    "Churchill_Sentai",
    "Benjamin",
    "Benjamin_DJ",
    "Ezili",
    "Ezili_SmudgeCat",
    "PatFusty",
    "PatFusty_Snowman",
    "Agent_Jericho",
    "Highwayman_Jericho",
  ]

  const heroPromises = heroes.map(async (hero) => {
    const { data, error } = await supabase.rpc("hero_totals", {
      hero: hero,
      map_name: map_name,
    })
    hero_counts[hero] = data[0]
  })

  await Promise.all(heroPromises)
  return new Response(JSON.stringify(hero_counts))
}
