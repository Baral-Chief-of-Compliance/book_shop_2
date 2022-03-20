from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from store.models import *
from . utils import cookieCart, cartData, guestOrder
from django.views.generic import ListView
from django.db.models import Q


def store(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products[:5], 'cartItems':cartItems,'order':order, 'items': items,}
    return render (request, 'store/store.html', context)


def book(request, book_id):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    book = Product.objects.get(id = book_id)
    context = {'book':book,'cartItems':cartItems,'order':order, 'items': items,}

    return render(request, 'store/book.html', context)


def catalog(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems':cartItems, 'order':order, 'items': items,}
    return render (request, 'store/catalog.html', context)

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order':order, 'cartItems':cartItems}
    return render (request, 'store/cart.html', context)



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render (request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False )

    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe = False)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False )

    else:
        customer, order = guestOrder(request, data)

    total = data['form']['total']
    order.transaction_id = transaction_id

    if (int(total) == int(order.get_cart_total)):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer = customer,
        order = order,
        address = data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode']
        )

    return JsonResponse('Payment subbmitted..', safe = False)





    template_name = 'store/search_results.html'

def get_queryset(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    quary = request.GET.get('q')
    object_list = Product.objects.filter(
        Q(name__icontains=quary)|Q(author__icontains=quary)
    )

    context = {'object_list':object_list,'cartItems':cartItems,'order':order, 'items': items,}

    return render (request, 'store/search_results.html', context)


    # def search_request(request):
