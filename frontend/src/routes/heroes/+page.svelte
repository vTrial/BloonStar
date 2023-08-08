<script>
  import FilterDropdown from "./../FilterDropdown.svelte"
  import Nav from "./../Nav.svelte"
  import TableStatsWhole from "./../TableStatsWhole.svelte"

  const mapsFilters = [
    ["", "All Maps"],
    ["banana_depot_scene", "Banana Depot"],
    ["basalt_columns", "Basalt Columns"],
    ["building_site_scene", "Building Site"],
    ["bloon_bot_factory", "Bloon Bot Factory"],
    ["castle_ruins", "Castle Ruins"],
    ["cobra_command", "Cobra Command"],
    ["dino_graveyard", "Dino Graveyard"],
    ["garden", "Garden"],
    ["glade", "Glade"],
    ["inflection", "Inflection"],
    ["koru", "Koru"],
    ["oasis", "Oasis"],
    ["ports", "Ports"],
    ["sands_of_time", "Sands of Time"],
    ["star", "Star"],
  ]
  let selectedMap = ""

  function handleFilterChanged(event) {
    selectedMap = event.detail
  }
</script>

<Nav />
<FilterDropdown
  on:filterChanged={handleFilterChanged}
  filterList={mapsFilters}
/>
<TableStatsWhole datatype="heroes" map={selectedMap} />
