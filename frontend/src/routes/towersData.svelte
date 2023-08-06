<script>
	import { onMount } from 'svelte';

	const get_fetch = async (url) => {
		const res = await fetch(url);
		if (res.ok) {
			return await res.json();
		} else {
			throw new Error(`Failed to fetch data from: ${url}`);
		}
	};

	const to_percent = (num) => {
		return (num * 100).toFixed(1) + '%';
	};

	let towersData;
	let matchCount;

	onMount(async () => {
		try {
			towersData = await get_fetch('http://localhost:5000/towers/get');
			matchCount = await get_fetch('http://localhost:5000/matches/count');
			towersData = Object.entries(towersData);
			towersData.sort((a, b) => b[1].games - a[1].games);
			console.log(towersData);
		} catch (error) {
			console.error(error);
		}
	});
</script>

{#if towersData && matchCount}
	{#each towersData as tower}
		<tr>
			<td>{tower[0]}</td>
			<td>{tower[1]['games']}</td>
			<td>{tower[1]['wins']}</td>
			<td>{to_percent(tower[1]['games'] / matchCount)}</td>
			<td>{to_percent(tower[1]['wins'] / tower[1]['games'])}</td>
		</tr>
	{/each}
{/if}
