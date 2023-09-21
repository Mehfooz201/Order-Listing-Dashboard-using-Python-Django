if (!$) {
    $ = django.jQuery;
}
$(document).ready(function () {
    // Function to update the amount field
    function updateAmount() {
        var subProductType = $('#id_product_sub_type').val();
        var quantity = $('#id_quantity').val();
        var currency = $('#id_currency').val();
        var deliveryTiming = $('#id_delivery_timing').val();
        var price = 0;
        var currencySymbol = '';

        // Price data for the selected delivery timing
        var deliveryTimingPrices = {
            '12HRS': {
                'Anatomic Full Crown': 6.0,
                'Veneer ( Emax, Ivoclar)': 6.0,
                'Inlay/Onlay': 6.0,
                'Smile Creator': 6.0,
                'Acrylic Temporary Crowns': 6.0,
                'Custom Implant Abutment': 7.0,

                'Cast Partial Denture Framework (upto 3 unit single arch)': 18.0,
                'Cast Partial Denture Framework (upto 6 unit single arch)': 18.0,
                'Cast Partial Denture Framework (upto 13 unit single arch)': 20.0,
                'Screw retained crown': 7.0,
                'All on 4/6 implants': 9.0,
                'Implant SLM malo bridge': 9.0,
                'Implant Hybrid Denture': 9.0,
                'Cast Partial Obturator': 9.0,
                'Bridge Framework': 7.0,
                'Bite Splint': 7.0,
                'Full Mouth Rehabilitation': 9.0,
                'Wax-up for smile correction': 9.0,

                'CO-CR framework': 9.0,
                'Zirconia Framework': 9.0,

                'Contact Model ( each quadrant )': 3.0,
                'Contact Model with extra die  ( each quadrant )': 3.0,
                'Models with articulation (uppr/lower)': 3.0,
                'Study Model (Full Mouth)': 3.0,
                'Surgical guide': 40.0,

                // Add more products and their prices for 12HRS delivery
            },

            '6HRS': {
                'Anatomic Full Crown': 7.0,
                'Veneer ( Emax, Ivoclar)': 7.0,
                'Inlay/Onlay': 7.0,
                'Smile Creator': 7.0,
                'Acrylic Temporary Crowns': 7.0,
                'Custom Implant Abutment': 9.0,

                'Cast Partial Denture Framework (upto 3 unit single arch)': 20.0,
                'Cast Partial Denture Framework (upto 6 unit single arch)': 20.0,
                'Cast Partial Denture Framework (upto 13 unit single arch)': 25.0,
                'Screw retained crown': 9.0,
                'All on 4/6 implants': 11.0,
                'Implant SLM malo bridge': 11.0,
                'Implant Hybrid Denture': 11.0,
                'Cast Partial Obturator': 11.0,
                'Bridge Framework': 9.0,
                'Bite Splint': 9.0,
                'Full Mouth Rehabilitation': 11.0,
                'Wax-up for smile correction': 11.0,

                'CO-CR framework': 11.0,
                'Zirconia Framework': 11.0,

                'Contact Model ( each quadrant )': 5.0,
                'Contact Model with extra die  ( each quadrant )': 5.0,
                'Models with articulation (uppr/lower)': 5.0,
                'Study Model (Full Mouth)': 5.0,
                'Surgical guide': 36.0,

                // Add more products and their prices for 6HRS delivery
            },
            '2HRS': {
                'Anatomic Full Crown': 9.0,
                'Veneer ( Emax, Ivoclar)': 9.0,
                'Inlay/Onlay': 9.0,
                'Smile Creator': 9.0,
                'Acrylic Temporary Crowns': 9.0,
                'Custom Implant Abutment': 11.0,

                'Cast Partial Denture Framework (upto 3 unit single arch)': 0.0,
                'Cast Partial Denture Framework (upto 6 unit single arch)': 0.0,
                'Cast Partial Denture Framework (upto 13 unit single arch)': 0.0,
                'Screw retained crown': 11.0,
                'All on 4/6 implants': 15.0,
                'Implant SLM malo bridge': 15.0,
                'Implant Hybrid Denture': 15.0,
                'Cast Partial Obturator': 15.0,
                'Bridge Framework': 11.0,
                'Bite Splint': 11.0,
                'Full Mouth Rehabilitation': 15.0,
                'Wax-up for smile correction': 15.0,


                'CO-CR framework': 15.0,
                'Zirconia Framework': 15.0,

                'Contact Model ( each quadrant )': 7.0,
                'Contact Model with extra die  ( each quadrant )': 7.0,
                'Models with articulation (uppr/lower)': 7.0,
                'Study Model (Full Mouth)': 7.0,
                'Surgical guide': 0.0,
                // Add more products and their prices for 2HRS delivery
            },
        };

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