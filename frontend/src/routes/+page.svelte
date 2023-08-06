<!DOCTYPE html>
<html lang="en">
	<head>
		<title>Tower Counts</title>
	</head>
	<body>
		<div id="table-container" />

		<script>
			async function fetchData() {
				try {
					const response = await fetch('http://localhost:5000/towers/get');
					if (!response.ok) {
						throw new Error('Network response was not ok');
					}
					const data = await response.json();
					createTable(data);
				} catch (error) {
					// Handle error
					console.error(error);
				}
			}

			// Function to create the HTML table
			async function createTable(data) {
				const tableContainer = document.getElementById('table-container');
				const table = document.createElement('table');
				let games = 0;
				try {
					const response = await fetch('http://localhost:5000/matches/count');
					if (!response.ok) {
						throw new Error('Network response was not ok');
					}
					games = await response.json();
				} catch (error) {
					// Handle error
					console.error(error);
				}
				console.log(games);
				// Table header
				const headerRow = table.insertRow();
				headerRow.insertCell().innerText = 'Tower Name';
				headerRow.insertCell().innerText = 'Games';
				headerRow.insertCell().innerText = 'Wins';
				headerRow.insertCell().innerText = 'Use rate';
				headerRow.insertCell().innerText = 'Win rate';

				// Table rows for each tower

				const dataArray = Object.entries(data);
				dataArray.sort((a, b) => b[1].games - a[1].games);
				console.log(dataArray);
				for (let towerIndex = 0; towerIndex < dataArray.length; towerIndex++) {
					const row = table.insertRow();
					row.insertCell().innerText = dataArray[towerIndex][0];
					row.insertCell().innerText = dataArray[towerIndex][1]['games'];
					row.insertCell().innerText = dataArray[towerIndex][1]['wins'];
					row.insertCell().innerText =
						((dataArray[towerIndex][1]['games'] / games) * 100).toFixed(1) + '%';
					row.insertCell().innerText =
						((dataArray[towerIndex][1]['wins'] / dataArray[towerIndex][1]['games']) * 100).toFixed(
							1
						) + '%';
				}

				tableContainer.appendChild(table);
			}

			// Call the function to create the table
			fetchData();
		</script>
	</body>
</html>
