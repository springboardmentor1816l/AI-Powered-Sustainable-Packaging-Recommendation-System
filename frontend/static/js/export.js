function exportToCSV() {
  const rows = [
    ["Rank", "Material", "Predicted Cost", "CO₂ Impact", "Sustainability"],
  ];

  document.querySelectorAll("#result-table-body tr").forEach((row) => {
    const cols = Array.from(row.children).map((td) => td.innerText);
    rows.push(cols);
  });

  const csvContent = rows.map((e) => e.join(",")).join("\n");
  const blob = new Blob([csvContent], { type: "text/csv" });

  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "sustainability_results.csv";
  link.click();
}

function exportToPDF() {
  window.print();
}
