<script>
    async function fetchData() {
        try {
        const response = await fetch('http://localhost:5000/matches');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        // Do something with the data
        console.log(data);
        } catch (error) {
        // Handle error
        console.error(error);
        }
    }
</script>

<button on:click={fetchData}>Fetch Data</button>