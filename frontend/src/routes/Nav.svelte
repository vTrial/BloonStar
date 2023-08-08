<nav>
  <div>
    <a href="/">Home</a>
  </div>
  <div>
    <a href="/towers">Towers</a>
  </div>
  <div>
    <a href="/heroes">Heroes</a>
  </div>
</nav>

<style>
  nav {
    display: grid;
    background-color: bisque;
    padding: 1em;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 1em;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    font-weight: bold;
  }
  a,
  a:visited,
  a:hover,
  a:active {
    color: inherit;
    text-decoration: none;
  }
</style>
