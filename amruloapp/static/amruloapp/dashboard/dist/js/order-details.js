$(function () {
    $("#order_daterange_input").daterangepicker(
      {
        timePicker: true,
        locale: {
          format: "YYYY-MM-DD HH:mm",
        },
      },
      function (start, end, label) {
        let msg = "start " + start.format("YYYY-MM-DD HH:mm");
        msg += "\n";
        msg += "end " + end.format("YYYY-MM-DD HH:mm");
  
        alert(msg);
      }
    );
  
    const dataTable = $("#orderListTable").DataTable({
      lengthChange: false,
      autoWidth: false,
      scrollX: true,
      buttons: ["csv", "pdf", "print"],
    });
  
    dataTable
      .buttons()
      .container()
      .appendTo("#orderListTable_wrapper .col-md-6:eq(0)");
  });
  