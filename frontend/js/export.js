function exportCSV() {
    const data = JSON.parse(localStorage.getItem("latest_recommendations")) || [];
    if (!data.length) return;

    const headers = Object.keys(data[0]);
    const rows = data.map(obj => headers.map(h => obj[h]));

    let csv = headers.join(",") + "\n";
    rows.forEach(r => csv += r.join(",") + "\n");

    const blob = new Blob([csv], {type:"text/csv"});
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "ecopack_analytics.csv";
    a.click();
}

function exportPDF() {
    window.print();
}
