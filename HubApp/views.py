from django.shortcuts import render
from django.http import HttpResponse
from .models import cart, orders, users,products
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.conf import settings  # new
from django.urls import reverse  # new
import stripe # new
import re






# Create your views here.
def home(request):
    return render(request,'login.html')





def register(request):
    if request.method == 'POST':
        Name = request.POST.get('name')
        Email = request.POST.get('mail')
        Number = request.POST.get('num')
        Password = request.POST.get('pass')
# 🔴 STEP 1: Name Validation (only letters, min 3 chars)
        if not re.match(r'^[A-Za-z]{3,30}$', Name):
            return HttpResponse("<script>alert('Name must contain only letters and at least 3 characters'); window.history.back();</script>")

        # 🔴 STEP 2: Email Validation (valid Gmail)
        if not re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', Email):
            return HttpResponse("<script>alert('Enter a valid Gmail address'); window.history.back();</script>")

        # 🔴 STEP 3: Phone Validation (10 digits only)
        if not re.match(r'^[0-9]{10}$', Number):
            return HttpResponse("<script>alert('Phone number must be exactly 10 digits'); window.history.back();</script>")

        # 🔴 STEP 4: Password Validation
        # At least 6 chars, 1 uppercase, 1 lowercase, 1 number
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{6,}$', Password):
            return HttpResponse("<script>alert('Password must contain 6+ characters, including uppercase, lowercase, and number'); window.history.back();</script>")
        # 🔴 STEP 5: Check duplicate email
        if users.objects.filter(email=Email).exists():
          return HttpResponse("<script>alert('Email already registered'); window.history.back();</script>")

        # ✅ Save data
        try:
            users.objects.create(
                name=Name,
                email=Email,
                number=Number,
                password=Password
            )
            return render(request, 'login.html')

        except Exception as e:
           return HttpResponse(f"<script>alert('Something went wrong: {e}'); window.history.back();</script>")

    return HttpResponse("<script>alert('Failed to Register'); window.history.back();</script>")




def customers(request):
    data = users.objects.all()
    
    
    paginator = Paginator(data, 3)   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users.html', {'page_obj': page_obj})




def login(request):
    if request.method == 'POST':
        Email = request.POST.get('mail')
        Password = request.POST.get('pass')

        admin_mail = 'admin123@gmail.com'
        admin_pass = 'admin'




         # 🔴 STEP 3: Admin Check
        if Email == admin_mail and Password == admin_pass:
            request.session['admin'] = True
            return render(request, 'admin.html')

        # 🔴 STEP 1: Email Validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', Email):
            return HttpResponse("<script>alert('Enter a valid Gmail address'); window.history.back();</script>")
        # 🔴 STEP 2: Password Validation
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{6,}$', Password):
            return HttpResponse("<script>alert('Invalid password format'); window.history.back();</script>")
    
       

        # 🔴 STEP 4: User Login Check
        try:
            data = users.objects.get(email=Email, password=Password)

            if data:
                request.session['uid'] = Email
                return render(request, 'index.html')

        except users.DoesNotExist:
            return HttpResponse('Invalid email or password')

    return HttpResponse("Login Failed")






def profile(request):
        if 'uid' in request.session:
            email = request.session['uid']
            user = users.objects.get(email=email)

            # 🔹 Handle form submission (update data)
            if request.method == "POST":
                user.name = request.POST.get('name')
                user.number = request.POST.get('number')
                user.email = request.POST.get('email')

                user.save()

            return render(request, 'profile.html', {'data': user})

def product_list(request):
    query = request.GET.get('q')

    if query:
        productitems = products.objects.filter(Q(product_name__icontains=query)|
                                               Q(description__icontains=query))
    else:
        productitems = products.objects.all()


    context={
        'products':productitems,
        'query':query
    }
    return render(request,'product.html',context)


def logout(request):
    if 'uid'in request.session:
        request.session.flush()
        return render(request,'login.html')









######   admin ######
def openaddproduct(request):
    return render(request,'addproduct.html')


def dashhh(request):
    return render(request,'admin.html')


def addproduct(request):
       
    if request.method == 'POST':
        Product = request.POST.get('product_name')
        Price = request.POST.get('price')
        Quantity = request.POST.get('quantity')
        Discription = request.POST.get('description')
        Images = request.FILES.get('image')
        id = request.POST.get('id')
        print(Images,'image')

        try: 
            data = products.objects.create(product_name=Product,price=Price,quantity=Quantity,description=Discription,images=Images,product_id=id)
            data.save()
            return HttpResponse('<script>alert("Product added successfully"); window.location="/addp";</script>')
        except Exception:
            return HttpResponse("somthing went wrong")
    return HttpResponse("Failed to Add Product")







def viewproduct(request):
    data = products.objects.all()
    return render(request, 'viewproduct.html', {'products': data})


def editproduct(request, id):
    product = get_object_or_404(products, id=id)

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.description = request.POST.get('description')

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        return redirect('viewproduct')

    return render(request, 'editproduct.html', {'product': product})


def deleteproduct(request, id):
    product = get_object_or_404(products, id=id)
    product.delete()
    return redirect('viewproduct')

    

def loglog(request):
    return render(request,'login.html')






def openbuy(request,id):
    product = products.objects.get(id=id)
    return render(request,'buy.html',{'product':product})
    
    
def buy(request, id):
    if request.method == 'POST':
        try:
            product = products.objects.get(id=id)
        except products.DoesNotExist:
            return HttpResponse('Product not found')

        if 'uid' in request.session:
            usermail = request.session['uid']
            user = users.objects.get(email=usermail)

            quantity = int(request.POST.get('quantity'))
            address = request.POST.get('address')

            try:
                
                order = orders.objects.create(
                    product=product,
                    user=user,
                    quantity=quantity,
                    address=address
                )

              
                stripe.api_key = settings.STRIPE_SECRET_KEY

                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            'price': product.product_id,  
                            'quantity': quantity,
                        },
                    ],
                    mode='payment',
                    success_url=request.build_absolute_uri(
                        reverse('payment_success')
                    ) + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri(
                        reverse('payment_cancel')
                    ),
                    metadata={
                        'order_id': order.id
                    }
                )

                return redirect(checkout_session.url, code=303)

            except Exception as e:
                print(e)
                return HttpResponse('Failed to place order')

        else:
            return HttpResponse('Please login to continue')

    return HttpResponse('Invalid request method')





def addtocart(request,id):
    if 'uid' in request.session:
        data=request.session['uid'] 
        user = users.objects.get(email=data)
        product = products.objects.get(id=id)

        shop = cart.objects.filter(user = user,product=product).first()

        if shop:
            shop.quantity +=1
            shop.save()

        else:
            cart.objects.create(user = user,product = product)
        return redirect('cartt')
    return redirect('login')







def order(request):
    data = orders.objects.all()
    return render(request, 'orders.html', {'product': data})




def Cart(request):
    return render(request,"cart.html")
    
    



def payment_success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    session_id = request.GET.get('session_id')
    if not session_id:
        return HttpResponse("Invalid payment session")

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        order_id = session.metadata.order_id
        order = orders.objects.get(id=order_id)

        if session.payment_status == 'paid':
            order.status = 'paid'
            order.save()
            return redirect('order_view')
        else:
            order.status = 'failed'
            order.save()
            return render(request, 'payment_failed.html')

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


def payment_cancel(request):
    return render(request, 'payment_failed.html')






def forgot_password(request):
    error = ""

    if request.method == "POST":
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")

        try:
            user = users.objects.get(email=email)
            user.password = new_password   # ⚠ Not secure (plain text)
            user.save()

            return redirect('login')   # 👈 Redirect to login page

        except users.DoesNotExist:
            error = "Email not found!"

    return render(request, "forgot_password.html", {
        "error": error
    })






def cart_view(request):
    uid = request.session.get('uid')   # safer way

    items = []
    total = 0   # ✅ initialize total

    if uid:
        user = users.objects.filter(email=uid).first()

        if user:
            items = cart.objects.filter(user=user)

            for item in items:
                item.price = item.quantity * item.product.price
                total += item.price

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })



def oder_view(request):
    
    uid = request.session['uid']

    user = users.objects.filter(email=uid).first()

    if user:
        orders_list = orders.objects.filter(user=user)
    else:
        orders_list = []

    return render(request,'order_view.html',{'orders':orders_list})




def indexload(request):
    return render(request, 'index.html')




def increase_qty(request, id):
    item = get_object_or_404(cart, id=id)
    
    item.quantity += 1 
    item.price = item.quantity * item.product.price  # increase quantity
    item.save()

    return redirect('/cartt')


def decrease_qty(request, id):
    item = get_object_or_404(cart, id=id)

    # Decrease quantity
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        # Optional: delete item if quantity becomes 0
        item.delete()

    return redirect('/cartt')   # change to your cart URL name


def remove_cart(request, id):
    item = get_object_or_404(cart, id=id)
    item.delete()
    return redirect('/cartt')








from django.shortcuts import get_object_or_404, redirect
from .models import orders

def update_status(request, id):
    order = get_object_or_404(orders, id=id)

    if request.method == "POST":
        new_status = request.POST.get('status')

        if new_status:
            order.Shipping = new_status   # update shipping status
            order.save()

    return redirect('/orders')



def cancel_order(request, id):
    order = get_object_or_404(orders, id=id)

    # Prevent cancelling after delivery
    if order.status != 'delivered':
        order.status = 'cancelled'
        order.save()

    return redirect('/order_view')





def cate_all(request, category):
    data = products.objects.filter(
        category__name=category
    ).all()
    return render(request,'category.html', {'products': data})



