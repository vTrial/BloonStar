<script>
  export let datatype
  function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1)
  }
</script>

<div class="table-header">{capitalize(datatype)}</div>
<div class="table-header">Matches</div>
<div class="table-header">Use rate</div>
<div class="table-header">Win rate</div>

<style>
  @font-face {
    font-family: "Montserrat-SemiBold"; /* Define a font family name */
    src: url("../fonts/Montserrat-SemiBold.ttf") format("truetype"); /* Path to your font file */
    /* You can also include other font formats for better cross-browser support */
  }
  .table-header {
    font-family: "Montserrat-SemiBold", sans-serif;
  }
</style>
