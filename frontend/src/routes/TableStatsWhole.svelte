<script>
  import TableStatsData from "./TableStatsData.svelte"
  import TableStatsHeader from "./TableStatsHeader.svelte"
  export let datatype
  export let map
</script>

<table id="table-container">
  <TableStatsHeader {datatype} />
  <TableStatsData {datatype} {map} />
</table>
