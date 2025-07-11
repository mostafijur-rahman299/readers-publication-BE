from cart.models import Cart
from payment.models import Payment
from rest_framework import serializers
from .models import Order, OrderStatus
from .models import OrderItem
from shipping.models import Shipping
from core.models import GeneralData
from django.utils import timezone


class OrderCreateSerializer(serializers.ModelSerializer):
    shipping_address_id = serializers.CharField(required=True, allow_null=False, write_only=True)
    payment_method = serializers.CharField(required=True, allow_null=False, write_only=True)
    mobile_number = serializers.CharField(allow_null=True, required=False, allow_blank=True, write_only=True)
    reference_number = serializers.CharField(allow_null=True, required=False, allow_blank=True, write_only=True)
    
    class Meta:
        model = Order
        fields = ['order_id', 'shipping_address_id', 'payment_method', 'mobile_number', 'reference_number']
        read_only_fields = ['order_id']
        
    def validate(self, attrs):
        payment_method = attrs.get('payment_method')
        if payment_method not in ['bkash', 'nagad', 'rocket', 'cod']:
            raise serializers.ValidationError("Invalid payment method")
        
        if payment_method in ['bkash', 'nagad', 'rocket']:
            if not attrs.get('mobile_number') or not attrs.get('reference_number'):
                raise serializers.ValidationError("Mobile number and reference number are required for mobile payment")
            
        shipping_address_id = attrs.get('shipping_address_id')
        shipping_address = Shipping.objects.filter(id=shipping_address_id, user=self.context['request'].user).first()
        if not shipping_address:
            raise serializers.ValidationError("Your shipping address is not valid")
        
        # get cart items
        cart_items = Cart.objects.filter(user=self.context['request'].user, is_selected=True)
        if not cart_items.exists():
            raise serializers.ValidationError("No cart items found")
        
        attrs['shipping_address'] = shipping_address
        del attrs['shipping_address_id']
                
        return attrs
    
    def create(self, validated_data):
        payment_method = validated_data.pop('payment_method')
        mobile_number = validated_data.pop('mobile_number')
        reference_number = validated_data.pop('reference_number')
        
        # get cart items
        cart_items = Cart.objects.filter(user=self.context['request'].user, is_selected=True)
        # get total price
        sub_total = sum(item.book.get_book_price() * item.quantity for item in cart_items)
        general_data = GeneralData.objects.first()
        if general_data.delivery_charge:
            shipping_cost = general_data.delivery_charge
        else:
            shipping_cost = 0
        total_amount = sub_total + shipping_cost
        
        # create order
        order = Order.objects.create(
            user=self.context['request'].user,
            sub_total=sub_total,
            shipping_cost=shipping_cost,
            total_amount=total_amount,
            status=OrderStatus.PENDING,
            shipping_address=validated_data['shipping_address'],
        )
        
        # create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.get_book_price() * item.quantity,
            )
            
        # delete cart items
        cart_items.delete()
        
        # create payment
        payment = Payment.objects.create_payment(
            user=self.context['request'].user,
            amount=total_amount,
            payment_method=payment_method,
            payment_date=timezone.now(),
            mobile_number=mobile_number,
            reference_number=reference_number,
        )
        
        # update order with payment
        order.payment = payment
        order.save()
        return order
