<script>
  import FilterDropdown from "$lib/svelteTemplates/FilterDropdown.svelte"
  import Nav from "$lib/svelteTemplates/Nav.svelte"
  import TableStatsWhole from "$lib/svelteTemplates/TableStatsWhole.svelte"
  import { mapNames, towerNames } from "$lib/ThingAliases"
  let selectedMap = ""

  function handleFilterChanged(event) {
    selectedMap = event.detail
  }
</script>

<Nav />
<h1>Top Battles 2 Towers</h1>
<FilterDropdown on:filterChanged={handleFilterChanged} filterList={mapNames} />
<TableStatsWhole datatype="towers" map={selectedMap} thingNames={towerNames} />
