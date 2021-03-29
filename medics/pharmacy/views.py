from django.shortcuts import redirect, render

from .form import CreatePharmacyAdminForm, CreatePharmacyForm, CreateProductForm, CreateUserForm, CreateCustomerForm
from .filters import PharmacyFilter
from django.http import HttpResponse

from .models import *

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.http import JsonResponse
import json
import datetime


from .utils import cookieCart, cartData, guestOrder
# Create your views here.
from django.views.decorators.csrf import csrf_protect

from django.core.paginator import Paginator
# Pharmacy Register
global_shop = None


def pharmacyRegister(request):

    form = CreatePharmacyAdminForm()
    form_p = CreatePharmacyForm()
    if request.method == 'POST':
        form = CreatePharmacyAdminForm(request.POST)
        form_P = CreatePharmacyForm(request.POST, request.FILES)

        if form.is_valid() and form_P.is_valid():
            user = form.save()
            # form_P.save()
            # username = form.cleaned_data.get('username')

            shop_name = form_P.cleaned_data.get('shop_name')
            phone = form_P.cleaned_data.get('phone')
            address = form_P.cleaned_data.get('address')
            area = form_P.cleaned_data.get('area')
            profile_pic = form_P.cleaned_data.get('profile_pic')

            # print(user)

            Pharmacy.objects.create(
                user=user,
                shop_name=shop_name, phone=phone, address=address, area=area, profile_pic=profile_pic
            )

            return HttpResponse('Success')

    context = {
        'form': form,
        'form_p': form_p
    }
    return render(request, 'pharmacy/pharmacyRegister.html', context)

# Pharmacy Login


def pharmacyLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('pharmacy_home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'pharmacy/pharmacyLogin.html', context)

# PHARMACY HOME


def pharmacyHome(request):
    products = request.user.pharmacy.product_set.all()

    context = {
        'products': products
    }
    return render(request, 'pharmacy/pharmacyHome.html', context)


# HOME

def home(request):

    pharmecy = Pharmacy.objects.all()

    myFilter = PharmacyFilter(request.GET, queryset=pharmecy)
    pharmecy = myFilter.qs
    context = {
        'pharmecy': pharmecy,
        'myFilter': myFilter,


    }

    return render(request, 'pharmacy/home.html', context)

# PHARMACY LOGOUT


def pharmacyLogout(request):

    logout(request)
    return redirect('pharmacy_login')

# PHARMACY ADD PRODUCTION


def pharmacyAddProduct(request):
    form = CreateProductForm()
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():

            user = request.user

            shop_name = Pharmacy.objects.get(user=user)
            print(shop_name)
            print(type(shop_name))

            name = form.cleaned_data.get('name')
            price = form.cleaned_data.get('price')
            category = form.cleaned_data.get('category')
            description = form.cleaned_data.get('description')
            image = form.cleaned_data.get('image')

            product = Product.objects.create(shop=shop_name, name=name, price=price,
                                             category=category, description=description, image=image)
            # product.shop.add(shop_name)

            return redirect("pharmacy_addproduct")

    context = {'form': form}
    return render(request, 'pharmacy/pharmacyAddProduct.html', context)


# PHARMACY DASHBOARD

def pharmacyDashboard(request):
    user = request.user

    print(user)

    pharmecy = Pharmacy.objects.get(user=user)

    print(pharmecy)

    orders = Order.objects.filter(shop=pharmecy)

    context = {'user': user, 'orders': orders}

    return render(request, 'pharmacy/pharmacyDashboard.html', context)


def pharmacyDashboardOrderItems(request, id):

    order = Order.objects.get(id=id)

    order_items = order.orderitem_set.all()
    context = {'order_items': order_items}
    return render(request, 'pharmacy/pharmacyOrderItems.html', context)


def pharmacyDashboardOrderAddress(request, id):
    order = Order.objects.get(id=id)
    address = order.shippingaddress_set.all()
    context = {'address': address}

    return render(request, 'pharmacy/pharmacyOrderAddress.html', context)


# Shop

def shop(request, id):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    shop = Pharmacy.objects.get(id=id)

    shop_id = shop.id

    products = None

    category = Category.objects.all()

    categoryID = request.GET.get('category')

    if categoryID:
        products = shop.product_set.filter(category=categoryID)

    else:
        products = shop.product_set.all()

    all_posts = products.order_by('id')
    paginator = Paginator(all_posts, 4, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'products': products, 'page_obj': page_obj, 'categorys': category,
               'shop': shop,  'shop_id': shop_id, 'cartItems': cartItems}

    return render(request, 'pharmacy/shop.html', context)


# SINGLE PRODUCT VIEW

def SingleProduct(request, id, pid):
    shop = Pharmacy.objects.get(id=id)
    product = Product.objects.get(id=pid)

    context = {
        'product': product,

    }
    return render(request, 'pharmacy/productSinglePage.html', context)
# Customer


def customerRegister(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # Added username after video because of error returning customer name if not added
            Customer.objects.create(
                user=user,
                name=user.username,
            )

            messages.success(request, 'Account was created for ' + username)

            return redirect('customer_login')

    context = {'form': form}
    return render(request, 'pharmacy/customerRegister.html', context)


def customerLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'pharmacy/customerLogin.html', context)


def customerLogout(request):

    logout(request)
    return redirect('customer_login')


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'pharmacy/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'pharmacy/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)

    productId = data['productId']
    action = data['action']
    pharmacy = data['pharmacy']

    print('Action:', action)
    print('Product:', productId)
    print('pharmacy:', pharmacy)

    customer = request.user.customer
    print("Customer", customer, type(customer))

    pharmacyId = Pharmacy.objects.get(id=pharmacy)

    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    order.shop = pharmacyId
    order.save()

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],

            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)
