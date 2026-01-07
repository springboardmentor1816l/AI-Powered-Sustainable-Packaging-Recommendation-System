const data = JSON.parse(localStorage.getItem("recommendationData"));

if (!data || !data.predictions || data.predictions.length === 0) {
    document.querySelector("main").innerHTML =
        "<p>No recommendations available.</p>";
} else {
    const tableBody = document.querySelector("#resultsTable tbody");

    data.predictions.forEach(item => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${item.rank}</td>
            <td>${item.material}</td>
            <td>₹${item.predicted_cost}</td>
            <td>${item.co2}</td>
            <td>${item.sustainability_score}</td>
        `;

        // Highlight best recommendation
        if (item.rank === 1) {
            row.style.backgroundColor = "#e6f4ea";
            row.style.fontWeight = "bold";
        }

        tableBody.appendChild(row);
    });
}
