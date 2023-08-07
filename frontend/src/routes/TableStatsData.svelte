<script>
  import { onMount, beforeUpdate } from "svelte"
  export let datatype
  export let map
  let endpoint = `http://localhost:5000/${datatype}/get/${map}`
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
      endpoint = `http://localhost:5000/${datatype}/get/${map}`
      fetchData()
    }
  })
</script>

{#if dataList}
  {#each dataList as data}
    <tr>
      <td>{data["name"]}</td>
      <td>{data["games"]}</td>
      <td>{data["wins"]}</td>
      <td>{to_percent(data["games"] / total_games)}</td>
      <td>{to_percent(data["wins"] / data["games"])}</td>
    </tr>
  {/each}
{/if}
