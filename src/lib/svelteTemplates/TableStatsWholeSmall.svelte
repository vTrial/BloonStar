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
    padding: 20px 20px 0px 20px; /* Add some padding around the grid */
    background-color: #f0f0f0; /* Add a background color for the container */
    border-radius: 10px; /* Rounded corners */
    margin: 1em 1em 2em 1em;
    align-items: stretch;
  }
</style>
