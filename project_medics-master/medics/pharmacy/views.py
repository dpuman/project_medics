from django.shortcuts import redirect, render

from .form import CreatePharmacyAdminForm, CreatePharmacyForm, CreateProductForm, CreateUserForm, UpdateOrder, CreateCustomerForm, UpdateCustomerForm, UpdatePharmacyForm
from .filters import PharmacyFilter, ProductFilter, PharmacyProductFilter
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

from django.forms import inlineformset_factory

# global_shop = None
# Pharmacy Register


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

            return redirect('pharmacy_login')

    context = {
        'form': form,
        'form_p': form_p
    }
    return render(request, 'pharmacy/pharmacyRegister.html', context)

# Pharmacy Login


def pharmacyLogin(request):
    try:
        user = request.user
        phar = Pharmacy.objects.get(user=user)
        print(user)
        print(phar)
        if request.user.is_authenticated and Pharmacy.objects.get(user=user):
            print('Hey', phar)
            return redirect('pharmacy_home')
    except:
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

    myFilter = PharmacyProductFilter(request.GET, queryset=products)
    products = myFilter.qs

    context = {
        'products': products,
        'myFilter': myFilter,
    }
    return render(request, 'pharmacy/pharmacyHome.html', context)


# Shop HOME

def home(request):

    pharmecy = Pharmacy.objects.all()

    myFilter = PharmacyFilter(request.GET, queryset=pharmecy)
    pharmecy = myFilter.qs
    context = {
        'pharmecy': pharmecy,
        'myFilter': myFilter,


    }

    return render(request, 'pharmacy/home.html', context)


# Pharmacy
def pharmacyProfile(request):

    user = request.user
    context = {
        'user': user
    }
    return render(request, 'pharmacy/pharmacyProfile.html', context)


def pharmacyProfileEdit(request, id):
    pharmacy = Pharmacy.objects.get(id=id)
    form = UpdatePharmacyForm(instance=pharmacy)

    if request.method == 'POST':
        form = UpdatePharmacyForm(
            request.POST, request.FILES, instance=pharmacy)
        if form.is_valid():
            form.save()
        return redirect('pharmacy_Profile')

    context = {'form': form}

    return render(request, 'pharmacy/pharmacyProfileEdit.html', context)

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


def pharmacyAddMultiProduct(request):
    ProductFormSet = inlineformset_factory(
        Pharmacy, Product, fields=('name', 'price', 'category', 'description', 'image'), can_delete=False, extra=20)
    pharmacy = request.user.pharmacy
    print("pharmacy", pharmacy)

    formset = ProductFormSet(queryset=Order.objects.none(), instance=pharmacy)

    if request.method == 'POST':
        formset = ProductFormSet(
            request.POST, request.FILES, instance=pharmacy)
        if formset.is_valid():
            formset.save()
            return redirect('pharmacy_add_multi_product')

    context = {'form': formset}

    return render(request, 'pharmacy/pharmacyAddMultiProduct.html', context)


# PHARMACY PRODUCT ACTIONS


def pharmacyProductUpdate(request, id):
    product = Product.objects.get(id=id)
    form = CreateProductForm(instance=product)

    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
        return redirect('pharmacy_home')

    context = {'form': form}
    return render(request, 'pharmacy/pharmacyProductUpdate.html', context)


def pharmacyProductDelete(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('pharmacy_home')

    context = {'product': product}

    return render(request, 'pharmacy/pharmacyProductDelete.html', context)


# PHARMACY DASHBOARD


def pharmacyDashboard(request):
    user = request.user

    print(user)

    pharmecy = Pharmacy.objects.get(user=user)

    print(pharmecy)

    orders = Order.objects.filter(shop=pharmecy)

    orders = orders.filter(delivary_status=False).filter(
        complete=True).order_by('date_ordered')

    total_orders = orders.count()

    context = {'user': user, 'orders': orders, 'total_orders': total_orders}

    return render(request, 'pharmacy/pharmacyDashboard.html', context)


def pharmacyDashboardUpdateOrder(request, id):
    order = Order.objects.get(id=id)
    form = UpdateOrder(instance=order)

    if request.method == 'POST':
        form = UpdateOrder(request.POST, instance=order)
        if form.is_valid():
            form.save()
        return redirect('pharmacy_dashboard')
    context = {'form': form}
    return render(request, 'pharmacy/pharmacyDashboardOrderUpdate.html', context)


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


def pharmacyDeliveredDashboard(request):
    user = request.user

    print(user)

    pharmecy = Pharmacy.objects.get(user=user)

    print(pharmecy)

    orders = Order.objects.filter(shop=pharmecy)

    orders = orders.filter(delivary_status=True)
    total = orders.count()

    context = {'user': user, 'orders': orders, 'total': total}

    return render(request, 'pharmacy/pharmacyDeliveredDashboard.html', context)


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

    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs

    all_posts = products.order_by('id')
    paginator = Paginator(all_posts, 6, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'products': products, 'page_obj': page_obj, 'categorys': category,
               'shop': shop,  'shop_id': shop_id, 'cartItems': cartItems, 'myFilter': myFilter}

    return render(request, 'pharmacy/shop.html', context)


# SINGLE PRODUCT VIEW

def SingleProduct(request, id, pid):
    data = cartData(request)
    cartItems = data['cartItems']
    shop = Pharmacy.objects.get(id=id)
    shop_id = shop.id
    product = Product.objects.get(id=pid)

    context = {
        'product': product,
        'cartItems': cartItems,
        'shop_id': shop_id,

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
    try:
        user = request.user
        print(user)
        val = Customer.objects.get(user=user)
        print("Hey", val)

        if request.user.is_authenticated and Customer.objects.get(user=user):

            print("Okay")
            return redirect('home')
    except:
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


def customerProfile(request):
    data = cartData(request)
    cartItems = data['cartItems']

    user = request.user

    context = {'cartItems': cartItems, 'user': user}
    return render(request, 'pharmacy/customerProfile.html', context)


def customerProfileEdit(request, id):

    customer = Customer.objects.get(id=id)

    form = UpdateCustomerForm(instance=customer)
    if request.method == 'POST':

        form = UpdateCustomerForm(
            request.POST, request.FILES, instance=customer)
        if form.is_valid():

            form.save()
        return redirect('customer_profile')

    context = {'form': form}
    return render(request, 'pharmacy/customerProfileEdit.html', context)


def customerLogout(request):

    logout(request)
    return redirect('customer_login')

# Shop Order Management


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
            phone=data['shipping']['phone'],
        )

    return JsonResponse('Payment submitted..', safe=False)
