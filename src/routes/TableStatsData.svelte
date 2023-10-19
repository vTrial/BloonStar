<script>
  import { onMount, beforeUpdate } from "svelte"
  export let datatype
  export let map
  export let thingNames
  let endpoint = `/api/get/${datatype}?map=${map}`
  let total_games = 1
  let dataList = []
  const fetchData = async () => {
    const response = await fetch(endpoint)
    const dataJson = await response.json()
    dataList = Object.entries(dataJson).map(([name, stats]) => ({
      name,
      ...stats,
    }))
    dataList.sort((a, b) => b.games - a.games)
    total_games = dataList.reduce((total, data) => total + data.games, 0)
    if (datatype == "towers") total_games /= 3
  }
  const to_percent = (num) => {
    return (num * 100).toFixed(1) + "%"
  }

  onMount(() => {
    fetchData()
  })

  let prevMap = map

  beforeUpdate(() => {
    if (map !== prevMap) {
      prevMap = map
      endpoint = `/api/get/${datatype}?map=${map}`
      fetchData()
    }
  })
</script>

{#if dataList}
  {#each dataList as data, index}
    <div class="table-data">{thingNames[data["name"]]}</div>
    <div class="table-data">{data["games"]}</div>
    <div class="table-data">{to_percent(data["games"] / total_games)}</div>
    <div class="table-data">{to_percent(data["wins"] / data["games"])}</div>
  {/each}
{/if}

<style>
  .table-data {
    font-family: Arial, Helvetica, sans-serif;
  }
</style>
