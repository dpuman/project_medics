import json
from .models import *


def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])

    except:

        cart = {}
        print('CART:', cart)

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, }
    cartItems = order['get_cart_items']
    pharmacy_Id = None

    print('CART:', cart)
    for i in cart.values():
        print("i", i)
        for key, value in i.items():
            try:
                print("j", key, 'vai', value)
                print(type(value), value['quantity'])
                cartItems += value['quantity']

                product = Product.objects.get(id=key)
                total = (product.price * value['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += value['quantity']

                # pharmacy = Pharmacy.objects.get(id=product.shop)
                pharmacyId = product.shop
                pharmacy_Id = pharmacyId.id
                print(pharmacy_Id)

                item = {
                    'id': product.id,
                    'product': {'id': product.id, 'name': product.name, 'price': product.price, 'imageURL': product.imageURL, 'shop': {'id': pharmacy_Id}}, 'quantity': value['quantity'], 'get_total': total,
                }
                items.append(item)
            except:
                pass

    return {'cartItems': cartItems, 'order': order, 'items': items, 'pharmacy_Id': pharmacy_Id}


def cartData(request):
    pharmacy_Id = None
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        pharmacy_Id = cookieData['pharmacy_Id']

    return {'cartItems': cartItems, 'order': order, 'items': items, 'pharmacy_Id': pharmacy_Id}


def guestOrder(request, data):
    print('User is not logged in')
    print("COOKIE", request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    pharmacy_Id = cookieData['pharmacy_Id']
    pharmecy = Pharmacy.objects.get(id=pharmacy_Id)

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
    order.shop = pharmecy
    order.save()

    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )

    return customer, order
