<script>
	const get_fetch = async (url) => {
		const res = await fetch(url);
		if (res.ok) {
			return await res.json();
		} else {
			throw new Error('Request failed');
		}
	};
	const towers = [
		'DartMonkey',
		'BoomerangMonkey',
		'BombShooter',
		'TackShooter',
		'IceMonkey',
		'GlueGunner',
		'SniperMonkey',
		'MonkeySub',
		'MonkeyBuccaneer',
		'MonkeyAce',
		'HeliPilot',
		'MortarMonkey',
		'DartlingGunner',
		'WizardMonkey',
		'SuperMonkey',
		'NinjaMonkey',
		'Alchemist',
		'Druid',
		'BananaFarm',
		'SpikeFactory',
		'MonkeyVillage',
		'EngineerMonkey'
	];
	const towers_data_promise = get_fetch('http://localhost:5000/towers/get');
</script>

<table id="table-container">
	{#await towers_data_promise then towers_data}
		{#each towers as tower}
			<tr>
				<td>{tower}</td>
				<td>{towers_data[tower]['games']}</td>
				<td>{towers_data[tower]['wins']}</td>
			</tr>
		{/each}
	{/await}
</table>
