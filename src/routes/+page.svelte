<script>
  import TableStatsWholeSmall from "$lib/svelteTemplates/TableStatsWholeSmall.svelte"
  import { heroNames, towerNames } from "$lib/ThingAliases"
</script>

<h1>Top Heroes</h1>
<a class="btn" href="/heroes">View Hero Stats</a>
<TableStatsWholeSmall datatype="heroes" map="" thingNames={heroNames} />
<h1>Top Towers</h1>
<a class="btn" href="/towers">View Tower Stats</a>
<TableStatsWholeSmall datatype="towers" map="" thingNames={towerNames} />

<style>
  a.btn {
    display: block;
    width: 10em;
    background: #b6c471;
    padding: 0.5em;
    text-align: center;
    border-radius: 5px;
    font-weight: bold;
    line-height: 25px;
    margin: 0em 0em 0em 1em;
  }
  h1 {
    margin: 0.5em;
  }
</style>