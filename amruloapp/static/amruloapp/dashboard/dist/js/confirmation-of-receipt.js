$(function() {
    const dataTable = $("#orderListTable").DataTable({
        lengthChange: false,
        autoWidth: false,
        scrollX: true,
        fixedColumns: {
            left: 1,
            right: 1,
        },
    });

    dataTable
        .buttons()
        .container()
        .appendTo("#orderListTable_wrapper .col-md-6:eq(0)");
});