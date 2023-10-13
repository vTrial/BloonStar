import { supabase } from "$lib/supabaseClient"
import { pastTime } from "$lib/sevenDaysAgo"
import { towerNames } from "$lib/ThingAliases"

export const GET = async ({ url }) => {
  const towers = Object.keys(towerNames)
  const map_name = url.searchParams.get("map") ?? ""
  // Define tower_counts object to store tower data
  const tower_counts = {}
  // Iterate over tower names from b2_consts.towers
  const towerPromises = towers.map(async (tower) => {
    const { data, error } = await supabase.rpc("tower_totals", {
      tower: tower,
      map_name: map_name,
      time_cutoff: pastTime,
    })
    tower_counts[tower] = data[0]
  })

  await Promise.all(towerPromises)

  return new Response(JSON.stringify(tower_counts))
}
