<script>
  import { createEventDispatcher } from "svelte"
  const dispatch = createEventDispatcher()
  export let filterList = []
  let selectedFilter = ""

  const changedFilter = () => {
    dispatch("filterChanged", selectedFilter)
  }
</script>

<select
  class="filter-dropdown"
  bind:value={selectedFilter}
  on:change={changedFilter}
>
  {#each filterList as filter}
    <option value={filter[0]}>{filter[1]}</option>
  {/each}
</select>

<style>
  .filter-dropdown {
    padding: 0.5em 4em 0.5em 0.5em;
    font-size: 1em;
  }
</style>
