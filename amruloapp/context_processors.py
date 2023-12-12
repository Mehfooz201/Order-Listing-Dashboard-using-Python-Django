from products.models import (DeliveryTiming,Product)

def amruloapp_context(request):
    inr_rate = 83.12  # You can use a default value here or handle the error as per your requirement

    delivery_timing = DeliveryTiming.objects.all()
    products = Product.objects.all()
    data_product_price = []
    for j in delivery_timing:
        data_product_price.append({str(j.id):{str(i.product_sub_type.id):i.product_12hrs_price.delivery_timing.name == j.name and float(i.product_12hrs_price.price) or i.product_6hrs_price.delivery_timing.name == j.name and float(i.product_6hrs_price.price) or i.product_2hrs_price.delivery_timing.name == j.name and float(i.product_2hrs_price.price) for i in products }})

    format_data1 = str(data_product_price).replace('[','')
    format_data2 = format_data1.replace(']','')
    format_data3 = format_data2.replace("}}, {","}, ")
    format_data4 = format_data3.replace("}}, {","}, ")
    format_data5 = format_data4.replace("'","\"")
    format_data6 = str(format_data5).replace("\'"," ")

    return dict(prod_price = format_data6, inrRate = inr_rate)
