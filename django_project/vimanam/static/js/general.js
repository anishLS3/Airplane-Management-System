document.addEventListener("DOMContentLoaded", () => {
    const tableRows = document.querySelectorAll("tr[data-href]");

    tableRows.forEach(row => {
        row.addEventListener("click", () => {
            window.location.href = row.dataset.href
        })
        row.style.cursor = "pointer";
    })

})