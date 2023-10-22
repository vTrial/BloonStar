<script>
	import Nav from "$lib/svelteTemplates/Nav.svelte"
	import Footer from "$lib/svelteTemplates/Footer.svelte"
</script>

<main>
	<div class="page1">
		<Nav/>
		<slot></slot>
	</div>
	<Footer/>
</main>

<style>
	/* make footer sticky */
	.page1 {
		display: flex;
		flex-direction: column;
		min-height: 95vh;
	}
	main {
		flex-grow: 1;
	}
</style>