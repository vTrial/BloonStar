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

	let heroesData;
	let matchCount;

	onMount(async () => {
		try {
			heroesData = await get_fetch('http://localhost:5000/heroes/get');
			matchCount = await get_fetch('http://localhost:5000/matches/count');
			heroesData = Object.entries(heroesData);
			heroesData.sort((a, b) => b[1].games - a[1].games);
		} catch (error) {
			console.error(error);
		}
	});
</script>

{#if heroesData && matchCount}
	{#each heroesData as hero}
		<tr>
			<td>{hero[0]}</td>
			<td>{hero[1]['games']}</td>
			<td>{hero[1]['wins']}</td>
			<td>{to_percent(hero[1]['games'] / matchCount)}</td>
			<td>{to_percent(hero[1]['wins'] / hero[1]['games'])}</td>
		</tr>
	{/each}
{/if}
