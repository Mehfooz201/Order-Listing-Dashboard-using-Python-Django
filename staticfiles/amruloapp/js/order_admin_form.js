if (!$) {
    $ = django.jQuery;
}

$(document).ready(function () {
    var el = document.getElementById('data_prices');
    var data = el.dataset;
    var originalPrice = $('#id_price').val();
    // Function to update the amount field
    function updateAmount() {
        var subProductType = $('#id_product_sub_type').val();
        var quantity = $('#id_quantity').val();
        var currency = $('#id_currency').val();
        var deliveryTiming = $('#id_delivery_timing').val();
        var price = 0;
        var remakePrice = 0;
        var currencySymbol = '';

        // Price data for the selected delivery timing
        var curr = parseFloat(data.currency);
        var data_price = JSON.parse(data.prices);
        var deliveryTimingPrices = data_price;
        // Get the base price for the selected product and delivery timing
        // Get the base price for the selected product and delivery timing
        var basePrice = deliveryTimingPrices[deliveryTiming][subProductType];

        if (basePrice !== undefined) {
            // Calculate the total price
            price = parseFloat(basePrice * quantity);

            // Get the currency symbol based on the selected currency
            if (currency === 'USA') {
                price *= 1;
            } else if (currency === 'INR') {
                currencySymbol = '₹'; // Indian Rupee symbol
                // Fetch the actual exchange rate for INR from your Django code
                var inrRate = curr; // Replace this with the actual exchange rate
                price *= parseFloat(inrRate);
            }

            if(parseFloat(price) > parseFloat(originalPrice)){
                remakePrice = parseFloat(price - originalPrice);
            }else{
                remakePrice = 0 ;
            }
        }

        

        // Update the amount field with the calculated price and currency symbol
        $('#id_price').val(price.toFixed(2));
        

        // Update delivery timing options based on the selected product type and its price for '2HRS'
        $('#id_delivery_timing option').each(function () {
            var optionValue = $(this).val();
            if (optionValue === '2HRS') {
                if (basePrice === undefined || deliveryTimingPrices['2HRS'][subProductType] === 0) {
                    // Hide the '2HRS' option if it has a zero price for the selected product type
                    $(this).hide();
                } else {
                    $(this).show();
                }
            }
        });

        // Update remake price field
        $('#id_remake_price').val(remakePrice.toFixed(2));
        
    }

    $("#id_product_sub_type").change(function () {
        updateAmount();
    });
    $("#id_quantity").change(function () {
        updateAmount();
    });
    $("#id_currency").change(function () {
        updateAmount();
    });
    $("#id_delivery_timing").change(function () {
        updateAmount();
    });

    function change() {
        var photos_field = $('#id_photos');
        photos_field.attr('multiple',true)
        var design_requirement_field = $('#id_design_requirement');
        design_requirement_field.attr('multiple',true)
        var file_upload_required_field = $('#id_file_upload_required');
        file_upload_required_field.attr('multiple',true)
    }
    change();

    $("#id_photos").change(function () {
        change();
    });
    $("#id_photos").click(function () {
        change();
    });
    $("#id_photos").mouseover(function () {
        change();
    });
    $("#id_photos").focus(function () {
        change();
    });

    $("#id_design_requirement").change(function () {
        change();
    });
    $("#id_design_requirement").click(function () {
        change();
    });
    $("#id_design_requirement").mouseover(function () {
        change();
    });
    $("#id_design_requirement").focus(function () {
        change();
    });

    $("#id_file_upload_required").change(function () {
        change();
    });
    $("#id_file_upload_required").click(function () {
        change();
    });
    $("#id_file_upload_required").mouseover(function () {
        change();
    });
    $("#id_file_upload_required").focus(function () {
        change();
    });
    
});