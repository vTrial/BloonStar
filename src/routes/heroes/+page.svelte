<script>
  import FilterDropdown from "$lib/svelteTemplates/FilterDropdown.svelte"
  import TableStatsWhole from "$lib/svelteTemplates/TableStatsWhole.svelte"
  import { mapNames, heroNames } from "$lib/ThingAliases"
  let selectedMap = ""

  function handleFilterChanged(event) {
    selectedMap = event.detail
  }
</script>

<h1>Top Battles 2 Heroes</h1>
<FilterDropdown on:filterChanged={handleFilterChanged} filterList={mapNames} />
<TableStatsWhole datatype="heroes" map={selectedMap} thingNames={heroNames} />
