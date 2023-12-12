const btnExportPDF = document.getElementById("btnExportPDF");
const jsPDF = jspdf.jsPDF;

btnExportPDF.addEventListener("click", function () {
  const element = document.getElementById("framework-agreement-card");
  const pdf = new jsPDF();
  pdf.html(element, {
    callback: function (pdf) {
      pdf.save("a4.pdf");
    },
  });
});
