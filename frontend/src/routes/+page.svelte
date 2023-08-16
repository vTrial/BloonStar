<script>
  import Nav from "./Nav.svelte"
  import TableStatsWholeSmall from "./TableStatsWholeSmall.svelte"
  import { heroNames, towerNames } from "./../utils/ThingAliases"
</script>

<Nav />
<a class="btn" href="/heroes">View Hero Stats</a>
<h1>Top Heroes</h1>
<TableStatsWholeSmall datatype="heroes" map="" thingNames={heroNames} />
<a class="btn" href="/towers">View Tower Stats</a>
<h1>Top Towers</h1>
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
  }
  h1 {
    margin: 0.5em;
  }
</style>
