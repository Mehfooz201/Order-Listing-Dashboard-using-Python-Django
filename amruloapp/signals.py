from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from notifications.signals import notify
from amruloapp.models import Order, User

@receiver(post_save, sender=Order)
def order_create( sender, instance, created, **kwargs):
    if created:
        notify.send(instance.user, recipient=instance.user,
        verb='New order created by '+str(instance.user))

@receiver(pre_save, sender=Order)
def cache_previous_mode(sender, instance, *args, **kwargs):
    original_remake_notes = None
    original_num_crowns = None
    original_num_brackets = None
    original_order_status = None
    if instance.pk:
        #-------Remake_notes value before save
        original_remake_notes = Order.objects.get(pk=instance.pk).remake_notes
        instance.__original_remake_notes = original_remake_notes
        #-------Num_crowns value before save
        original_num_crowns = Order.objects.get(pk=instance.pk).num_crowns
        instance.__original_num_crowns = original_num_crowns
        #-------Remake_notes value before save
        original_num_brackets = Order.objects.get(pk=instance.pk).num_brackets
        instance.__original_num_brackets = original_num_brackets
        #-------Order_status value before save
        original_order_status = Order.objects.get(pk=instance.pk).order_status
        instance.__original_order_status = original_order_status
        

@receiver(post_save, sender=Order)
def post_save_mode_handler(sender, instance, created, **kwargs):
    #-------If order approved,cancelled or completed
    if (instance.order_status != instance.__original_order_status and instance.__original_order_status !='approved' and instance.order_status == 'approved' or
        instance.order_status != instance.__original_order_status and instance.__original_order_status !='cancelled' and instance.order_status == 'cancelled' or
        instance.order_status != instance.__original_order_status and instance.__original_order_status !='completed' and instance.order_status == 'completed' ):
        notify.send(instance.user, recipient=instance.user, verb='Order '+ str(instance.order_status))
    else:
        pass
    #-------If original (Remake_notes, Num_crowns and Remake_notes ) values change
    if (instance.remake_notes != instance.__original_remake_notes or
        instance.num_crowns != instance.__original_num_crowns or
        instance.num_brackets != instance.__original_num_brackets ):
        notify.send(instance.user, recipient=instance.user, verb='Order remake requested by '+ str(instance.user.username)+ ' for order N°'+str(instance.pk))
    else:
        pass