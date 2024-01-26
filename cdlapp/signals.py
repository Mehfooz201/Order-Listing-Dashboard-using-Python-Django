from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from notifications.signals import notify
from cdlapp.models import Order, User
from django.core.mail import send_mail
from django.urls import reverse

@receiver(post_save,sender=User)
def save_user(sender,instance, created,**kwargs):
    if created:
        #pass_ = instance.user_password
        #instance.set_password(pass_)
        #instance.user_password =" "
        #instance.confirm_password=" "
        instance.save()


@receiver(post_save, sender=Order)
def order_create( sender, instance, created, **kwargs):
    if created:
        notify.send(instance.user, recipient=instance.user,
        verb='New order created by ' + str(instance.user)) + 'Order No. ' + str(instance.pk)


        subject = "Order has been created"
        
        # Get the absolute URL for the homepage
        homepage_url = "http://127.0.0.1:8000"  # Replace with your actual website URL
        order_details_url = reverse('order-detail', kwargs={'order_number': instance.pk})
        order_details_full_url = f"{homepage_url}{order_details_url}"

        
        message = (
            f"Hello {instance.user.username},\n\n"
            f"Thank you for placing an order. Here are your order details:\n\n"
            f"Customer Username: {instance.user.username}\n"
            f"Email: {instance.user.email}\n"
            f"New order has been created with Order No. {instance.pk}.\n"
            f"Please visit our website at: {order_details_full_url}\n\n"  # Include the URL here
            f"Best regards,\nConfident Dental Laboratory (Pvt.) Ltd"
        )
        from_email = "admin@design.confidentlab.com"  # Change to your admin's email address
        recipient_list = [instance.user.email]
        send_mail(subject, message, from_email, recipient_list)



@receiver(pre_save, sender=Order)
def cache_previous_mode(sender, instance, *args, **kwargs):
    global original_remake_notes
    global original_num_crowns
    global original_num_brackets
    global original_order_status
    global original_price
    original_remake_notes = None
    original_num_crowns = None
    original_num_brackets = None
    original_order_status = None
    original_price = 0
    if instance.pk:
        #-------Remake_notes value before save
        original_remake_notes = Order.objects.get(pk=instance.pk).remake_notes
        #-------Num_crowns value before save
        original_num_crowns = Order.objects.get(pk=instance.pk).num_crowns
        #-------Remake_notes value before save
        original_num_brackets = Order.objects.get(pk=instance.pk).num_brackets
        #-------Order_status value before save
        original_order_status = Order.objects.get(pk=instance.pk).order_status
        #-------Order_price value before save
        original_price = Order.objects.get(pk=instance.pk).price
        

@receiver(post_save, sender=Order)
def post_save_mode_handler(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        #-------If order approved,cancelled or completed
        if (instance.order_status != original_order_status and original_order_status !='approved' and instance.order_status == 'approved' or
            instance.order_status != original_order_status and original_order_status !='cancelled' and instance.order_status == 'cancelled' or
            instance.order_status != original_order_status and original_order_status !='completed' and instance.order_status == 'completed' ):
            notify.send(instance.user, recipient=instance.user, verb='Order No. ' + str(instance.pk) + ' ' + str(instance.order_status))
            

            subject = "Update on Order"

            # Get the absolute URL for the homepage
            homepage_url = "http://127.0.0.1:8000"  # Replace with your actual website URL
            order_details_url = reverse('order-detail', kwargs={'order_number': instance.pk})
            order_details_full_url = f"{homepage_url}{order_details_url}"
            print('order_details_full_url', order_details_full_url)
            
            message = (
                f"Hello {instance.user.username},\n\n"
                f"Customer Username: {instance.user.username}\n"
                f"Email: {instance.user.email}\n"
                f"Order No. {instance.pk} has been updated. New status: {instance.order_status}\n\n"
                f"Please visit our website at: {order_details_full_url}\n\n"  # Include the URL here
                f"Best regards,\nConfident Dental Laboratory (Pvt.) Ltd"
            )
            from_email = "admin@design.confidentlab.com"  # Change to your admin's email address
            recipient_list = [instance.user.email]
            send_mail(subject, message, from_email, recipient_list)


        else:
            pass
        #-------If original (Remake_notes, Num_crowns and Remake_notes ) values change
        if (instance.remake_notes != original_remake_notes or
            instance.num_crowns != original_num_crowns or
            instance.num_brackets != original_num_brackets ):
            notify.send(instance.user, recipient=instance.user, verb='Order remake requested by '+ str(instance.user.username)+ ' for Order No. '+str(instance.pk))

            subject = "Update on Order"

            # Get the absolute URL for the homepage
            homepage_url = "http://127.0.0.1:8000"  # Replace with your actual website URL
            order_details_url = reverse('order-detail', kwargs={'order_number': instance.pk})
            order_details_full_url = f"{homepage_url}{order_details_url}"
            
            message = (
                f"Hello {instance.user.username},\n\n"
                f"Customer Username: {instance.user.username}\n"
                f"Email: {instance.user.email}\n"
                f"Order No. {instance.pk} has been updated. New status: {instance.order_status}\n\n"
                f"Please visit our website at: {order_details_full_url}\n\n"  # Include the URL here
                f"Best regards,\nConfident Dental Laboratory (Pvt.) Ltd"
            )
            from_email = "admin@design.confidentlab.com"  # Change to your admin's email address
            recipient_list = [instance.user.email]
            send_mail(subject, message, from_email, recipient_list)

        else:
            pass
    
