$(function () {
    const hanleViewOrder = () => {
      $("#viewOrderModal").modal("show");
    };
    const handleRevoke = () => {
      const state = confirm("are you sure you want to revoke?");
      const msg = state ? "order has been revoked successfully" : "cancelled";
      alert(msg);
    };
    const dataTable = $("#orderListTable").DataTable({
      lengthChange: false,
      autoWidth: false,
      scrollX: true,
      fixedColumns: {
        left: 1,
        right: 1,
      },
      createdRow: (row, data, index) => {
        const menu = $("<div></div>");
        menu.addClass("datatable-actions-container");
        const btnView = $("<button></button>");
        btnView.html("View");
        btnView.addClass("btn-action");
  
        const btnRevoke = $("<button></button>");
        btnRevoke.html("Revoke");
        btnRevoke.addClass("btn-action");
  
        btnView.on("click", hanleViewOrder);
        btnRevoke.on("click", handleRevoke);
  
        menu.append(btnView).append(btnRevoke);
  
        $("td:last-child", row).html(menu);
      },
    });
  
    dataTable
      .buttons()
      .container()
      .appendTo("#orderListTable_wrapper .col-md-6:eq(0)");
  });
  