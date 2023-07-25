$(document).ready(function () {
  $(".quantity-left-minus").on("click", function () {
    const input = $(this)
      .closest(".inc-dec-button-group")
      .find(".input-number");
    const value = parseInt(input.val());
    if (isNaN(value)) {
        input.val(input.attr("min") || 0);
      } else {
        input.val(value - 1);
      }
  });
  $(".quantity-right-plus").on("click", function () {
    const input = $(this)
      .closest(".inc-dec-button-group")
      .find(".input-number");
    const value = parseInt(input.val());
    if (isNaN(value)) {
      input.val(input.attr("min") || 0);
    } else {
      input.val(value + 1);
    }
  });
});
