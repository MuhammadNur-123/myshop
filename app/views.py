
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View 
from .models import Customer, Product, Cart , OrderPlaced ,Contact ,NewsletterSubscription ,Blog,BlogTag
from .forms import CustomerRegistrationForm, CustomerProfileForm,ReviewForm,ContactForm,NewsletterSubscriptionForm, OrderPlacedForm ,ProductForm,BlogForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse ,HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 
from django.contrib.admin.views.decorators import staff_member_required

from django.http import Http404


def dashboard(request):
    total_customer = Customer.objects.count()  
    total_product = Product.objects.count() 
    total_order = OrderPlaced.objects.count() 
    total_card = Cart.objects.count() 
    total_contact = Contact.objects.count() 

    context = {
        'total_customer': total_customer,
        'total_product': total_product,
        'total_order': total_order,
        'total_card': total_card,
        'total_contact': total_contact,
    }

    return render(request, 'home/dashboard.html', context)

class ProductView(View):
       
    def get(self, request):
        totalitem = 0
        all_product = Product.objects.all()
        vegetable= Product.objects.filter(category='VEG')
        fruit= Product.objects.filter(category='FR')
        juice= Product.objects.filter(category='JU')
        teacofee = Product.objects.filter(category='TC')
        bread = Product.objects.filter(category='BRD')
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          

        return render(request,'home/home-4.html',{'all_product': all_product,'vegetable': vegetable,'fruit':fruit,'juice': juice,'teacofee':teacofee,'bread':bread,'totalitem':totalitem})
    

class ProductDetailView(View):
	def get(self, request, pk):
		totalitem = 0
		product = Product.objects.get(pk=pk)
		print(product.id)
		item_already_in_cart=False
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
			item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
		return render(request, 'product_details/product-details.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})
    
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product= Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    print(product)
    return redirect('/cart')


@login_required
def show_cart(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0.0
		shipping_amount = 30.0
		totalamount=0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		print(cart_product)
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity * p.product.discounted_price)
				amount += tempamount
			totalamount = amount+shipping_amount
			return render(request, 'cart/addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount, 'totalitem':totalitem})
		else:
			return render(request, 'cart/emptycart.html', {'totalitem':totalitem})
	else:
		return render(request, 'cart/emptycart.html', {'totalitem':totalitem})


def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1
		c.save()
		amount = 0.0
		shipping_amount= 30.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			
			amount += tempamount
		
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 30.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
		
			amount += tempamount
		
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount= 30.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
		
			amount += tempamount
		
		data = {
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")                



def vegetable(request,data=None):
    if data== None:
        vegetables = Product.objects.filter(category='VEG')
    elif data == 'Tomato' or data== 'Fulkopy':
        vegetables = Product.objects.filter(food_brand= data) 
    return render(request,'vegetable/product_vegetable.html',{'vegetables':vegetables})
        
def fruit(request,data=None):
    if data== None:
        fruits = Product.objects.filter(category='FR')
    elif data == 'Banana' or data== 'Apple':
        fruits = Product.objects.filter(food_brand= data) 
    return render(request,'fruits/product_fruits.html',{'fruits':fruits})

def juice(request,data=None):
    if data== None:
        juices = Product.objects.filter(category='JU')
    elif data == 'Apple Juice' or data== 'Tomato Juice':
        juices = Product.objects.filter(food_brand= data) 
    return render(request,'juice/product_juice.html',{'juices':juices})

def tea(request,data=None):
    if data== None:
        teas = Product.objects.filter(category='TC')
    elif data == 'Tea' or data== 'Tea Black':
        teas = Product.objects.filter(food_brand= data) 
    return render(request,'tea/product_tea.html',{'teas':teas})

def bread(request,data=None):
    if data== None:
        breads = Product.objects.filter(category='BRD')
    elif data == 'Brown Bread' or data== 'White Bread':
        breads = Product.objects.filter(food_brand= data) 
    return render(request,'bread/product_bread.html',{'breads':breads})

def jam(request,data=None):
    if data== None:
        jams = Product.objects.filter(category='JAM')
    elif data == 'Apple Jam' or data== 'Orange Jam':
        jams = Product.objects.filter(food_brand= data) 
    return render(request,'jam/product_jam.html',{'jams':jams})  

def product_grid(request):
    all_products = Product.objects.all()
    return render(request,'product_details/product-grid-left-sidebar.html',{'all_products':all_products})


@login_required
def checkout(request):
	user = request.user
	add = Customer.objects.filter(user=user)
	cart_items = Cart.objects.filter(user=request.user)
	amount = 0.0
	shipping_amount = 30.0
	totalamount=0.0
	cart_product = [p for p in Cart.objects.all() if p.user == request.user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
		totalamount = amount+shipping_amount
	return render(request, 'product_details/checkout.html', {'add':add, 'cart_items':cart_items, 'totalcost':totalamount})

@login_required
def orders(request):
	op = OrderPlaced.objects.filter(user=request.user)
	return render(request, 'cart/orders.html', {'order_placed':op})

 

# List orders
@staff_member_required
def order_list(request):
    orders = OrderPlaced.objects.all()
    return render(request, 'cart/order_list.html', {'orders': orders})

# Update order
@staff_member_required
def order_update(request, id):
    order = get_object_or_404(OrderPlaced, id=id)
    if request.method == 'POST':
        form = OrderPlacedForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderPlacedForm(instance=order)
    return render(request, 'cart/update_from.html', {'form': form})

# Delete order
@staff_member_required
def order_delete(request, id):
    order = get_object_or_404(OrderPlaced, id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'cart/delete.html', {'order': order})

@login_required
def payment_done(request):
    custid = request.GET.get('custid')

    # Handle missing `custid`
    if not custid:
        messages.error(request, "Customer ID is missing. Please try again.")
        return redirect('cart')  # Redirect to the cart page or any other appropriate page

    try:
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        messages.error(request, "Invalid Customer ID. Please try again.")
        return redirect('cart')

    user = request.user
    cart_items = Cart.objects.filter(user=user)

    for cart_item in cart_items:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=cart_item.product,
            quantity=cart_item.quantity
        )
        cart_item.delete()  # Delete cart items after creating orders

    messages.success(request, "Your order has been placed successfully.")
    return redirect("orders")

# @login_required
# def payment_done(request):
     
# 	custid = request.GET.get('custid')
# 	print("Customer ID", custid)
# 	user = request.user
# 	cartid = Cart.objects.filter(user = user)
# 	customer = Customer.objects.get(id=custid)
# 	print(customer)
# 	for cid in cartid:
# 		OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
# 		print("Order Saved")
# 		cid.delete()
# 		print("Cart Item Deleted")
# 	return redirect("orders")
   
       
      

def about(request):
    return render(request,'about/page-about-us.html')


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'profile/address.html',{'add':add,'active':'btn-primary'})




@staff_member_required
def customer_list(request):
    customers = Customer.objects.all()  # Fetch all customer records
    return render(request, 'login/customer_list.html', {'customers': customers})


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'login/customer_registration.html',{'form':form})
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! registered Successfully')     
            form.save()
        return render(request,'login/customer_registration.html',{'form':form})        

# List products
@staff_member_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_details/product_list.html', {'products': products})

# Create product
@staff_member_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_details/product_form.html', {'form': form})

# Update product
@staff_member_required
def product_update(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_details/product_form.html', {'form': form})

# Delete product
@staff_member_required
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request,f'Product "{product.title}" has been successfully deleted.')
        return redirect('product_list')
    return render(request, 'product_details/product_delete.html', {'product': product})
   



@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'profile/profile.html',{'form':form,'active':'btn-primary'})
    
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']             
            locality = form.cleaned_data['locality']             
            city = form.cleaned_data['city']             
            zipcode = form.cleaned_data['zipcode']             
            division= form.cleaned_data['division']
            reg= Customer(user=usr, name=name, locality=locality, city=city, division=division, zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations!! Profile Update Succcessfully')
        return render(request,'profile/profile.html',{'form':form,'active':'btn-primary'})                 
         
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})


@staff_member_required
def view_messages(request):
    messages_list = Contact.objects.all() 
   
    unread_count = Contact.objects.filter(read=False).count()
    if unread_count > 0:
        messages.success(request, f"You have {unread_count} new messages!")

    # Mark all messages as read
    Contact.objects.filter(read=False).update(read=True)
    messages.success(request, "Messages loaded successfully")
    return render(request, 'contact/message.html', {'messages': messages_list})



def product_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()  # Fetch related reviews
    return render(request, 'product_details/product-details.html', {'product': product, 'reviews': reviews})

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_reviews', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'product_details/product-details.html', {'form': form, 'product': product})



# List subscriptions
@staff_member_required
def subscription_list(request):
    subscriptions = NewsletterSubscription.objects.all().order_by('-subscribed_at')
    return render(request, 'contact/subscription_list.html', {'subscriptions': subscriptions})

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            
            # Check if the email already exists
            if NewsletterSubscription.objects.filter(email=email).exists():
                messages.error(request, 'You are already subscribed to the newsletter.')
            else:
                form.save()
                messages.success(request, 'Thank you for subscribing to our newsletter!')
            return redirect('home')  # Redirect to homepage or any other page
    else:
        form = NewsletterSubscriptionForm()
    
    return render(request, 'common_code/base.html', {'form': form})


def blog_list(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'blog/blog_list.html', context)

# Blog Detail View
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog/blog.html',{ 'blog':blog})

# Create Blog View
@staff_member_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            form.save_m2m()  
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})

