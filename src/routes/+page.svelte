<script>
  import Nav from "$lib/svelteTemplates/Nav.svelte"
  import TableStatsWholeSmall from "$lib/svelteTemplates/TableStatsWholeSmall.svelte"
  import { heroNames, towerNames } from "$lib/ThingAliases"
  import Footer from "$lib/svelteTemplates/Footer.svelte"
</script>

<Nav />
<h1>Top Heroes</h1>
<a class="btn" href="/heroes">View Hero Stats</a>
<TableStatsWholeSmall datatype="heroes" map="" thingNames={heroNames} />
<h1>Top Towers</h1>
<a class="btn" href="/towers">View Tower Stats</a>
<TableStatsWholeSmall datatype="towers" map="" thingNames={towerNames} />
<Footer/>
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
