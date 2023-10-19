<script>
  import FilterDropdown from "./../FilterDropdown.svelte"
  import Nav from "./../Nav.svelte"
  import TableStatsWhole from "./../TableStatsWhole.svelte"
  import { mapNames, heroNames } from "$lib/ThingAliases"
  let selectedMap = ""

  function handleFilterChanged(event) {
    selectedMap = event.detail
  }
</script>

<Nav />
<h1>Top Battles 2 Heroes</h1>
<FilterDropdown on:filterChanged={handleFilterChanged} filterList={mapNames} />
<TableStatsWhole datatype="heroes" map={selectedMap} thingNames={heroNames} />
