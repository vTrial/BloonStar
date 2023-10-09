import { supabase } from "$lib/supabaseClient"

export const GET = async ({ url }) => {
  const map_name = url.searchParams.get("map") ?? ""
  // Define tower_counts object to store tower data
  const tower_counts = {}
  const towers = [
    "DartMonkey",
    "BoomerangMonkey",
    "BombShooter",
    "TackShooter",
    "IceMonkey",
    "GlueGunner",
    "SniperMonkey",
    "MonkeySub",
    "MonkeyBuccaneer",
    "MonkeyAce",
    "HeliPilot",
    "MortarMonkey",
    "DartlingGunner",
    "WizardMonkey",
    "SuperMonkey",
    "NinjaMonkey",
    "Alchemist",
    "Druid",
    "BananaFarm",
    "SpikeFactory",
    "MonkeyVillage",
    "EngineerMonkey",
  ]
  // Iterate over tower names from b2_consts.towers
  for (const tower of towers) {
    // Create a Supabase query to fetch tower data
    // Execute the query and retrieve the result
    const { data, error } = await supabase.rpc("tower_totals", {
      tower: tower,
      map_name: map_name,
    })
    tower_counts[tower] = data[0]
  }
  return new Response(JSON.stringify(tower_counts))
}
