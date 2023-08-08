<script>
  import FilterDropdown from "./../FilterDropdown.svelte"
  import Nav from "./../Nav.svelte"
  import TableStatsWhole from "./../TableStatsWhole.svelte"
  import { mapNames, heroNames } from "./../../utils/ThingAliases"
  let selectedMap = ""

  function handleFilterChanged(event) {
    selectedMap = event.detail
  }
</script>

<Nav />
<FilterDropdown on:filterChanged={handleFilterChanged} filterList={mapNames} />
<TableStatsWhole datatype="heroes" map={selectedMap} thingNames={heroNames} />
