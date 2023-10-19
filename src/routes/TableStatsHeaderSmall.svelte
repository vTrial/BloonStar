<script>
  export let datatype
  function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1)
  }
</script>

<div class="table-header">{capitalize(datatype)}</div>
<div class="table-header">Use rate</div>
<div class="table-header">Win rate</div>

<style>
  .table-header {
    font-family: "Montserrat-SemiBold", sans-serif;
  }
</style>
