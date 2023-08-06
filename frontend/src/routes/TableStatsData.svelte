<script>
	import { onMount } from 'svelte';

	export let datatype;

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

	let dataList;
	let matchCount;

	onMount(async () => {
		try {
			dataList = await get_fetch(`http://localhost:5000/${datatype}/get`);
			matchCount = await get_fetch('http://localhost:5000/matches/count');
			dataList = Object.entries(dataList);
			dataList.sort((a, b) => b[1].games - a[1].games);
		} catch (error) {
			console.error(error);
		}
	});
</script>

{#if dataList && matchCount}
	{#each dataList as data}
		<tr>
			<td>{data[0]}</td>
			<td>{data[1]['games']}</td>
			<td>{data[1]['wins']}</td>
			<td>{to_percent(data[1]['games'] / matchCount)}</td>
			<td>{to_percent(data[1]['wins'] / data[1]['games'])}</td>
		</tr>
	{/each}
{/if}
