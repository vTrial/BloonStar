<script>
  import FilterDropdown from "./../FilterDropdown.svelte"
  import Nav from "./../Nav.svelte"
  import TableStatsWhole from "./../TableStatsWhole.svelte"
  import { mapNames, towerNames } from "./../../utils/ThingAliases"
  let selectedMap = ""

  function handleFilterChanged(event) {
    selectedMap = event.detail
  }
</script>

<Nav />
<h1>Top Battles 2 Towers</h1>
<FilterDropdown on:filterChanged={handleFilterChanged} filterList={mapNames} />
<TableStatsWhole datatype="towers" map={selectedMap} thingNames={towerNames} />
