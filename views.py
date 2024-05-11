from django.shortcuts import render
from elasticsearch_dsl import Search
from rest_framework import serializers, viewsets

from .documents import ProductDocument
from .models import *
from .serializer import *


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as loginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from .models import Category
from .models import Product
from .models import Cart
from .forms import ProductFilterForm
from .models import Order
from django.shortcuts import HttpResponse
from django.http import JsonResponse


#################### index#######################################

def index(request):
    return render(request, 'index.html')


########### register here #####################################

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            htmly = get_template('Email.html')
            d = {'username': username}
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            # msg.send()
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'title': 'register here'})


def login(request):
    # if request.method == 'POST':
    #     # AuthenticationForm_can_also_be_used__
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         form = login(request, user)
    #         messages.success(request, f' welcome {username} !!')
    #         return redirect('index')
    #
    #     else:
    #         messages.info(request, f'account done not exit plz sign in')
    # form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                loginView(request, user)
                messages.success(request, f'Welcome {username}!')
                return redirect('index')
            else:
                messages.info(request, 'Account does not exist. Please sign in.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def profile(request):
    return render(request, 'profile.html')


def user_profile(request):
    profile_data = {
        'profile_picture': request.GET.get('profilePicture', ''),
        'first_name': request.GET.get('firstName', ''),
        'last_name': request.GET.get('lastName', ''),
        'age': request.GET.get('age', ''),
        'dob': request.GET.get('dob', ''),
        'email': request.GET.get('email', ''),
        'phone_number': request.GET.get('phoneNumber', ''),
        'address': request.GET.get('address', ''),
    }

    return render(request, 'user_profile.html', {'profile_data': profile_data})


def has_profile(user):
    try:
        profile = user.profile
        return True
    except:
        return False


def profile_or_user_profile(request):
    if request.user.is_authenticated and has_profile(request.user):
        return redirect('user_profile')
    else:
        return redirect('profile')


def laptopuri_view(request):
    laptopuri_category = Category.objects.get(category='Laptop')
    laptopuri_products = Product.objects.filter(category=laptopuri_category).order_by('id')
    context = {'laptops': laptopuri_products}
    return render(request, 'laptopuri.html', context)


def telefoane_view(request):
    telefoane_category = Category.objects.get(category='Telefon')
    telefoane_products = Product.objects.filter(category=telefoane_category).order_by('id')
    context = {'phones': telefoane_products}
    return render(request, 'telefoane.html', context)


def search_view(request):
    search_text = request.POST.get('search_text', '')
    products = Product.objects.all()

    if search_text:
        products = products.filter(name__icontains=search_text)

    context = {'products': products, 'search_text': search_text}
    return render(request, 'search_results.html', context)


def product_list_view(request):
    products = Product.objects.all()
    form = ProductFilterForm()

    if request.method == 'POST':
        form = ProductFilterForm(request.POST)
        if form.is_valid():
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            min_stock = form.cleaned_data.get('min_stock')
            max_stock = form.cleaned_data.get('max_stock')
            supplier = form.cleaned_data.get('supplier')
            delivery_method = form.cleaned_data.get('delivery_method')

            if min_price:
                products = products.filter(price__gte=min_price)
            if max_price:
                products = products.filter(price__lte=max_price)
            if min_stock:
                products = products.filter(stock__gte=min_stock)
            if max_stock:
                products = products.filter(stock__lte=max_stock)
            if supplier:
                products = products.filter(supplier__icontains=supplier)
            if delivery_method:
                products = products.filter(delivery_method__icontains=delivery_method)

    context = {'products': products, 'form': form}
    return render(request, 'product_list.html', context)


def wishlist_view(request):
    product_name = request.GET.get('product_name')

    wishlist_products = request.session.get('wishlist_products', [])

    if product_name and product_name not in wishlist_products:
        wishlist_products.append(product_name)

    request.session['wishlist_products'] = wishlist_products

    return render(request, 'wishlist.html', {'wishlist_products': wishlist_products})


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)

        if request.user.is_authenticated:
            user_cart, created = Cart.objects.get_or_create(user=request.user, product=product, quantity=1)

            product.cart = user_cart
            product.save()

            return redirect('product_list')

        else:

            return render(request, 'login.html')


def cart_view(request):
    product = Product.objects.order_by('-name')
    user = request.user
    cart = Cart.objects.filter(user=user)

    total_price = sum(cart_item.total_price() for cart_item in cart)

    context = {'products': product,
               'user': user,
               'cart': cart,
               'total_price': total_price,
               }

    return render(request, 'cart.html', context)


def checkout(request):
    cart = request.session.get('cart', {})
    total_cost = sum(float(product_info['price']) for product_info in cart.values())
    return render(request, 'checkout.html', {'cart': cart, 'total_cost': total_cost})


def purchase(request):
    if request.method == 'POST':
        address = request.POST.get('address ')
        card_name = request.POST.get('card_name')
        card_id = request.POST.get('card_id ')
        expiration_date = request.POST.get('expiration_date')
        method_delivery = request.POST.get('method_delivery')
        bonus_cod = request.POST.get('bonus_cod')

        order = Order.objects.create(
            user=request.user,
            address=address,
            card_name=card_name,
            card_id=card_id,
            expiration_date=expiration_date,
            method_delivery=method_delivery,
            bonus_cod=bonus_cod
        )

        request.user.cart.products.clear()

        return HttpResponse(f'Comanda #{order.id} a fost plasată cu succes!')

    return redirect('history')


def history(request):
    user = request.user
    history = Order.objects.filter(user=user).order_by('-date')

    context = {
        'user': user,
        'history': history,
    }

    return render(request, 'history.html', context)


def search(request):
    query = request.GET.get('search_elastic')
    if query:
        intersected_product = ProductDocument.search().filter("term", description=query)
        # keywords = query.split()
        # ids_sets = []
        #
        # for keyword in keywords:
        #     s = Search().filter('term', descriptions=keyword)
        #     response = s.execute()
        #     ids_sets.append(set(hit.meta.id for hit in response))
        # if ids_sets:
        #     intersected_ids = set.intersection(*ids_sets)
        #     intersected_product = [hit for hit in response if hit.meta.id in intersected_ids]
        # else:
        #     intersected_product = []

    else:
        intersected_product = Product.objects.all()
    return render(request, 'searchresults.html', {'products': intersected_product, 'query': query})
