function startCSVExport() {

    document.getElementById("exportStatus").textContent =  "Downloading CSV...";
    window.location.href = "/export/csv";
    setTimeout(function () {
        document.getElementById("exportStatus").textContent ="CSV download started.";
        alert("CSV download started!");

    }, 500);
}


function startPDFExport() {

    document.getElementById("exportStatus").textContent = "Downloading PDF...";
    window.location.href = "/export/pdf";
    setTimeout(function () {

        document.getElementById("exportStatus").textContent = "PDF download started.";
        alert("PDF download started!");

    }, 500);
}