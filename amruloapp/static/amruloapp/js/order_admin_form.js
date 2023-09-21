if (!$) {
    $ = django.jQuery;
}

$(document).ready(function () {
    var el = document.getElementById('data_prices');
    var data = el.dataset;
    // Function to update the amount field
    function updateAmount() {
        var subProductType = $('#id_product_sub_type').val();
        var quantity = $('#id_quantity').val();
        var currency = $('#id_currency').val();
        var deliveryTiming = $('#id_delivery_timing').val();
        var price = 0;
        var currencySymbol = '';

        // Price data for the selected delivery timing
        var data_price = JSON.parse(data.prices);
        var deliveryTimingPrices = data_price;
        // Get the base price for the selected product and delivery timing
        // Get the base price for the selected product and delivery timing
        var basePrice = deliveryTimingPrices[deliveryTiming][subProductType];

        if (basePrice !== undefined) {
            // Calculate the total price
            price = basePrice * quantity;

            // Get the currency symbol based on the selected currency
            if (currency === 'USA') {
                price *= 1;
            } else if (currency === 'INR') {
                currencySymbol = '₹'; // Indian Rupee symbol
                // Fetch the actual exchange rate for INR from your Django code
                var inrRate = 82; // Replace this with the actual exchange rate
                price *= inrRate;
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
    
});