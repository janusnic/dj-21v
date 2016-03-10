from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            #order = form.save()
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch task
            order_created(order.id)
            return render(request, 'shop/orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'shop/orders/create.html', {'cart': cart,
                                                        'form': form})
