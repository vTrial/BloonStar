<script>
	export let datatype;
	function capitalize(string) {
		return string.charAt(0).toUpperCase() + string.slice(1);
	}
</script>

<tr>
	<th>{capitalize(datatype)}</th>
	<th>Matches</th>
	<th>Wins</th>
	<th>Use rate</th>
	<th>Win rate</th>
</tr>
