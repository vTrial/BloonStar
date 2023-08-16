<script>
  import TableStatsDataSmall from "./TableStatsDataSmall.svelte"
  import TableStatsHeaderSmall from "./TableStatsHeaderSmall.svelte"
  export let datatype
  export let map
  export let thingNames
</script>

<div class="table-stats-whole">
  <TableStatsHeaderSmall {datatype} />
  <TableStatsDataSmall {datatype} {map} {thingNames} />
</div>

<style>
  .table-stats-whole {
    display: grid;
    grid-template-columns: auto auto auto;
    grid-gap: 20px; /* Gap between items */
    padding: 1em; /* Add some padding around the grid */
    background-color: #f0f0f0; /* Add a background color for the container */
    border-radius: 10px; /* Rounded corners */
    margin: 1em 1em 2em 1em;
  }
</style>
