<script>
	const get_fetch = async (url) => {
		const res = await fetch(url);
		if (res.ok) {
			return await res.json();
		} else {
			throw new Error('Request failed');
		}
	};
	const towers_data_promise = get_fetch('http://localhost:5000/towers/get');
</script>

<table id="table-container">
	{#await towers_data_promise then towers_data}
		{#each Object.entries(towers_data) as [tower, data]}
			<tr>
				<td>{tower}</td>
				<td>{data['games']}</td>
				<td>{data['wins']}</td>
			</tr>
		{/each}
	{/await}
</table>
