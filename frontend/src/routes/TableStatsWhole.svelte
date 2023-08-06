<script>
	import TableStatsData from './TableStatsData.svelte';
	import TableStatsHeader from './TableStatsHeader.svelte';
	export let datatype;
</script>

<table id="table-container">
	<TableStatsHeader {datatype} />
	<TableStatsData {datatype} />
</table>
