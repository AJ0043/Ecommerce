from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.http.response import JsonResponse
from django.contrib import messages
from.models import *
from django.views.decorators.csrf import csrf_exempt
from Ecomapp.models import Contact
from Ecomapp.models import Feedback
from Ecomapp.models import Complaint
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Product, Cart
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from .Email import send_verification_email
from django.utils.encoding import force_str
from django .utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
import logging
import random
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from .models import Feedback
from datetime import date
from .models import Order
from django.core.mail import send_mail
import hashlib
logger = logging.getLogger(__name__)
from .forms import RegisterForm
#from razorpay import Client
from .models import Blog




def send_whatsapp_message(message):
    import requests

    # WhatsApp API Integration
    api_url = "https://api.twilio.com/2010-04-01/Accounts/your_account_sid/Messages.json"
    account_sid = "your_account_sid"  # Replace with your Twilio Account SID
    auth_token = "your_auth_token"  # Replace with your Twilio Auth Token
    from_whatsapp_number = "whatsapp:+14155238886"  # Twilio Sandbox Number
    to_whatsapp_number = "whatsapp:+918949167574"  # Admin's WhatsApp number

    data = {
        "From": from_whatsapp_number,
        "To": to_whatsapp_number,
        "Body": message,
    }

    response = requests.post(api_url, data=data, auth=(account_sid, auth_token))
    return response.status_code, response.text






def home(request):
    arrival = Arrival.objects.filter(status=0)
    demand = Demand .objects.filter(status=0)
    delership = Delership .objects.filter()
    context ={'Arrival':arrival,'Demand':demand,'Delership':delership}
    return render(request, 'index.html',context) 
 


def collections(request):
    category = Category.objects.filter(status=0)
    context = {'category': category}
    return render(request, "collections.html", context)


def collectionsview(request, slug):
        if(Category.objects.filter(slug=slug,status=0)):       
             products=Product.objects.filter(category__slug=slug)
             category_name = Category.objects.filter(slug=slug).first()
             context = {'products':products,'category_name':category_name}
             return render(request,'Store/Products/Index.html',context)
        else:
             messages.warning(request,"No Such Category Found")
             return redirect('collections')



@login_required(login_url='Login')
def productview(request, cate_slug, prod_slug):
    if Category.objects.filter(slug=cate_slug).exists():
        if Product.objects.filter(slug=prod_slug).exists():
            product = Product.objects.get(slug=prod_slug)
            context = {'product': product}
            return render(request, "Store/Products/view.html", context)
        else:
            messages.error(request, "No such product found")
            return HttpResponse('No such product found')
    else:
        messages.error(request, "No such category found")
        return redirect('collections')



def feature(request):
     return render(request,'Features.html')



def Aboutus(request):
     return render(request,'Aboutus.html')

@login_required(login_url='Login')
@csrf_exempt 
def Contactus(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        
        # Save contact details to the database
        contact = Contact(Name=name, Email=email, Phone=phone, Message=message)
        contact.save()
        
        # Message content
        message_content = f"""
        A new contact form submission has been received:

        Name: {name}
        Email: {email}
        Phone: {phone}
        Message: {message}

        Regards,
        Swastik Traders
        """

        # Send Email
        admin_email = "techstech506@gmail.com"
        mail_subject = "New Contact Us Form Submitted"
        mail = EmailMessage(mail_subject, message_content, to=[admin_email])
        mail.send()

        # Send WhatsApp Notification to Admin
       
        
        return redirect('success')  # Redirect to success page
    
    return render(request, 'Contact.html')


@login_required(login_url='Login')
@csrf_exempt 
def FeedbackView(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        product = request.POST['product']
        message = request.POST['message']
        
        # Create a new feedback instance and save it to the database
        feedback = Feedback(Name2=name, Email2=email, Phone2=phone, Product2=product, Message2=message)
        feedback.save()
        
        # Send feedback details to your email ID
        admin_email = "techstech506@gmail.com"  # Your email ID
        mail_subject = "New Feedback Received"
        mail_message = f"""
        A new feedback has been submitted:

        Name: {name}
        Email: {email}
        Phone: {phone}
        Product: {product}
        Message: {message}

        Regards,
        Swastik Traders
        """
        
        mail = EmailMessage(mail_subject, mail_message, to=[admin_email])
        mail.send()

        return redirect('Feedback')  # Redirect to the same page or any other desired page
    
    return render(request, 'Feedback.html')

@login_required(login_url='Login')
@csrf_exempt
def Complaint(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        product = request.POST.get('product')
        model = request.POST.get('model')
        message = request.POST.get('message')
        uploaded_file = request.FILES.get('image')
        
        if name and email and phone and product and model and message and uploaded_file:
            # Create a new Complaint instance and save it to the database
            complaint = Complaint(
                Name3=name,
                Email3=email,
                Phone3=phone,
                Product3=product,
                Model3=model,
                Message2=message,
                Image=uploaded_file
            )
            complaint.save()
            return redirect('home')
        else:
            return render(request, 'Complaint.html', {'error': 'All fields are required'})
    return render(request, 'Complaint.html')




########################## Authetication & Checkout ##############
def Login(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('log')

    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('wrong')

    return render(request, 'Login.html')





































def Signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        pass1 = request.POST.get('Password1')
        pass2 = request.POST.get('Password2')

        if not (name and email and pass1 and pass2):
            return HttpResponse("All fields are required!")
        
        if pass1 != pass2:
            return redirect('notmatch')
        
        my_user = User.objects.create_user(username=name, email=email, password=pass1)
        my_user.save()    
        
        # Send Verification Email #
        send_verification_email(request, my_user)
        
        return redirect("Login") 
    return render(request, 'Signup.html')


def activate(request, uidb64, token):
    try:
        # Decode the user's ID
        uid = force_str(urlsafe_base64_encode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('Login')  # Redirect to login page after activation
    else:
        return HttpResponse('Activation link is invalid!')



@csrf_exempt
def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect("home")



@login_required(login_url=Login)
def Cart2(request):
    if request.method == "POST":
        try:
            prod_id = int(request.POST.get('product_id'))
            prod_qty = int(request.POST.get('product_qty'))
            logger.info(f"Received POST request with product_id: {prod_id} and product_qty: {prod_qty}")
            product_check = get_object_or_404(Product, id=prod_id)
            logger.info(f"Product found: {product_check}")

            cart_item, created = Cart.objects.get_or_create(user=request.user, product_id=prod_id)

            if created:
                if product_check.quantity >= prod_qty:
                    cart_item.product_qty = prod_qty
                    cart_item.save()
                    logger.info("Product added to cart successfully")
                    return JsonResponse({"status": "Product added successfully"}, status=200)
                else:
                    logger.warning(f"Only {product_check.quantity} quantity available")
                    return JsonResponse({"status": f"Only {product_check.quantity} quantity available"}, status=400)
            else:
                new_qty = cart_item.product_qty + prod_qty
                if product_check.quantity >= new_qty:
                    cart_item.product_qty = new_qty
                    cart_item.save()
                    logger.info("Product quantity updated in cart")
                    return JsonResponse({"status": "Product quantity updated in cart"}, status=200)
                else:
                    logger.warning(f"Only {product_check.quantity} quantity available")
                    return JsonResponse({"status": f"Only {product_check.quantity} quantity available"}, status=400)

        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            return JsonResponse({"status": "Invalid input"}, status=400)
        except Exception as e:
            logger.error(f"Exception: {e}")
            return JsonResponse({"status": str(e)}, status=500)
    return render(request, '/')




def update_cart(request):
    if request.method == 'POST':
        prod_id = request.POST.get('product_id')
        prod_qty = request.POST.get('product_qty')
        
        if prod_qty is None:
            return JsonResponse({"status": "Product quantity is required"}, status=400)
        
        try:
            prod_qty = int(prod_qty)
        except ValueError:
            return JsonResponse({"status": "Invalid product quantity"}, status=400)
        
        if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({"status": "Updated Successfully"}, status=300)
        else:
            return JsonResponse({"status": "Product not found in cart"}, status=404)
    return JsonResponse({"status": "Invalid request method"}, status=400)

def delete_cart_item(request):
    if request.method == 'POST':
        prod_id = request.POST.get('product_id')
        
        if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.delete()
            return JsonResponse({"status": "Item removed successfully"}, status=300)
        else:
            return JsonResponse({"status": "Product not found in cart"}, status=404)
    return JsonResponse({"status": "Invalid request method"}, status=400)

@login_required(login_url=Login)
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {'cart': cart_items} 
    return render(request, 'Cart.html', context)


##################################### Checkout ###########################
















########################### Dashboard Views ############################







def Dash(request):
    return render(request,'Dash.html')




def complaint_list(request):
    return render(request, 'complaint_list.html')

def Customer(request):
    users = User.objects.all()
    return render(request,'Customer.html',{'users':users})


def order_list(request):
    orders = Order.objects.select_related('user').all()
    return render(request, 'order_list.html', {'orders': orders})
    


def contact_list_view(request):
    contacts = Contact.objects.all()  # Fetch all contacts from the database
    return render(request, 'contact_list.html', {'contacts': contacts})

def Feedback2(request):
    feedback_list = Feedback.objects.all()  # Fetch all feedback from the database
    return render(request, 'Feed_back.html', {'feedback_list': feedback_list})




############## DashBoard #########################




























############################### wishlist ##############################

@login_required(login_url=Login)
def Wishlists(request):
    Wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {'wishlist': Wishlist_items} 
    return render(request, 'Wishlist.html', context)


@login_required(login_url=Login)
def addWishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            try:
                product_check = Product.objects.get(id=prod_id)
                if Wishlist.objects.filter(user=request.user, product_id=prod_id).exists():
                    return JsonResponse({'status': "Product already in Wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status': "Product added to Wishlist successfully"})
            except Product.DoesNotExist:
                return JsonResponse({"status": "No such product"})
        else:
            return JsonResponse({"status": "Login to continue"})
    return redirect('/')


@csrf_exempt
def delete_list_item(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        wishlist_item = Wishlist.objects.get(product_id=product_id, user=request.user)
        wishlist_item.delete()
        return JsonResponse({'status': 'Item removed from wishlist'})
    return JsonResponse({'status': 'Invalid request'}, status=400)


@login_required(login_url='Login')
def Check(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Ensure the user is logged in

    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            item.delete()  # Correct way to delete the item

    cartitems = Cart.objects.filter(user=request.user)  # Corrected to use request.user
    total_price = 0
    for item in cartitems:
        total_price += item.product.Selling_Price * item.product_qty

    Userprofile = Profile.objects.filter(user=request.user).first()

    context = {'cartitems': cartitems, 'total_price': total_price, 'Userprofile' : Userprofile}
    return render(request, 'Checkout.html', context)



#razorpay_client = Client(auth=("YOUR_RAZORPAY_KEY", "YOUR_RAZORPAY_SECRET"))

@login_required(login_url='Login')
def placeorder2(request):
    if request.method == "POST":

        # Check payment status
        payment_mode = request.POST.get('payment_mode', 'COD')  # Default is COD
        payment_id = request.POST.get('razorpay_payment_id', None)
        payment_status = False

        if payment_mode == "Razorpay" and payment_id:
            try:
                # Verify Razorpay payment
                payment = razorpay_client.payment.fetch(payment_id)
                if payment["status"] == "captured":
                    payment_status = True
                else:
                    messages.error(request, "Payment verification failed. Please try again.")
                    return redirect('Cart')
            except Exception as e:
                messages.error(request, f"Error verifying payment: {str(e)}")
                return redirect('Cart')

        if payment_mode == "COD" or payment_status:
            # Update User Information
            CurrentUser = request.user

            if not CurrentUser.first_name:
                CurrentUser.first_name = request.POST.get('Fname')
                CurrentUser.last_name = request.POST.get('Lname')
                CurrentUser.save()

            # Update or Create Profile Information
            if not Profile.objects.filter(user=CurrentUser).exists():
                Userprofile = Profile(
                    user=CurrentUser,
                    phone=request.POST.get('Phone'),
                    address=request.POST.get('Address'),
                    city=request.POST.get('City'),
                    state=request.POST.get('State'),
                    country=request.POST.get('Country'),
                    pincode=request.POST.get('Pincode')
                )
                Userprofile.save()

            # Create a new Order
            neworder = Order(
                user=CurrentUser,
                Fname=request.POST.get('Fname'),
                Lname=request.POST.get('Lname'),
                Email=request.POST.get('Email'),
                Phone=request.POST.get('Phone'),
                Address=request.POST.get('Address'),
                City=request.POST.get('City'),
                State=request.POST.get('State'),
                Country=request.POST.get('Country'),
                Pincode=request.POST.get('Pincode'),
                Payment_mode=payment_mode,
                Payment_id=payment_id if payment_mode == "Razorpay" else None,
            )

            # Calculate total price
            cart = Cart.objects.filter(user=request.user)
            cart_total_price = sum(item.product.Selling_Price * item.product_qty for item in cart)
            neworder.Total_price = cart_total_price

            # Generate a unique tracking number
            trackno = 'AnveshJain' + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no=trackno).exists():
                trackno = 'AnveshJain' + str(random.randint(1111111, 9999999))
            neworder.tracking_no = trackno

            neworder.save()

            # Save order items
            order_items_details = ""
            for item in cart:
                Orderitem.objects.create(
                    order=neworder,
                    Product=item.product,
                    Price=item.product.Selling_Price,
                    Quantity=item.product_qty
                )
                # Update product quantity
                orderproduct = Product.objects.get(id=item.product_id)
                orderproduct.quantity -= item.product_qty
                orderproduct.save()

                # Add product details to the email body
                order_items_details += f"Product: {item.product.name}, Quantity: {item.product_qty}, Price: Rs {item.product.Selling_Price * item.product_qty}\n"

            # Clear the cart
            Cart.objects.filter(user=request.user).delete()

            # Send email for COD or Razorpay orders
            send_mail(
                subject="New Order Received",
                message=f"""
                A new order has been placed.

                Order Details:
                Name: {neworder.Fname} {neworder.Lname}
                Email: {neworder.Email}
                Phone: {neworder.Phone}
                Address: {neworder.Address}, {neworder.City}, {neworder.State}, {neworder.Country} - {neworder.Pincode}
                Total Price: Rs {neworder.Total_price}
                Tracking Number: {neworder.tracking_no}

                Ordered Products:
                {order_items_details}
                """,
                from_email="your-email@gmail.com",
                recipient_list=["techstech506@gmail.com"],
            )

            # Send order details to customer's email
            send_mail(
                subject="Your Order Confirmation",
                message=f"""
                Thank you for your order!

                Your order has been placed successfully with the following details:

                Order Details:
                Name: {neworder.Fname} {neworder.Lname}
                Email: {neworder.Email}
                Phone: {neworder.Phone}
                Address: {neworder.Address}, {neworder.City}, {neworder.State}, {neworder.Country} - {neworder.Pincode}
                Total Price: Rs {neworder.Total_price}
                Tracking Number: {neworder.tracking_no}

                Ordered Products:
                {order_items_details}
                """,
                from_email="techstech506@gmail.com",
                recipient_list=[neworder.Email],
            )

            # Success message
            messages.success(request, "Your order has been placed successfully.")
            return redirect('OrderSuccess')  # Redirect to a success page

        messages.error(request, "Payment failed or invalid request. Please try again.")
        return redirect('Cart')

def productlist(request):
    products = Product.objects.filter(status=0).values_list('name', flat=True)  # Use values_list
    productlist = list(products)
    return JsonResponse(productlist, safe=False)

def searchproduct(request):
    if request.method == 'POST':
        searcheditem = request.POST.get("searchproduct")
        if not searcheditem:
            return redirect(request.META.get('HTTP_REFERER'))  # Redirect to the previous page if search term is empty
        
        # Filter products where the name contains the search term
        products = Product.objects.filter(name__icontains=searcheditem)
        
        if products.exists():
            # If products exist, you might want to redirect to a search results page
            # This depends on how you want to display search results
            # For simplicity, we'll redirect to a results page
            return redirect(reverse('search_results') + f'?q={searcheditem}')
        else:
            messages.info(request, "No products matched your search")
            return redirect(request.META.get('HTTP_REFERER'))  # Redirect back to the previous page if no products found
    
    return redirect(request.META.get('HTTP_REFERER'))  # Redirect if not a POST request


def search_results(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'products': products, 'query': query})


##############################################################################










# its all about for Clipart messages #
@login_required(login_url='Login')
def Book(request):
     orders = Order.objects.filter(user=request.user)
     context = {'orders':orders}
     return render(request,'Book.html',context)

def vieworder(request, t_no):
    try:
        # Fetch the specific order for the logged-in user
        order = get_object_or_404(Order, tracking_no=t_no, user=request.user)
        orderitems = Orderitem.objects.filter(order=order)

        # Determine Payment Mode
        payment_mode = order.Payment_mode
        if payment_mode.lower() == "cod":
            payment_mode = "Cash on Delivery (COD)"
        elif payment_mode.lower() == "razorpay":
            payment_mode = "Razorpay"
        
        # Context dictionary to pass data to the template
        context = {
            'order': order,
            'orderitems': orderitems,
            'payment_mode': payment_mode,
        }

    except Exception as e:
        logging.error(f"Error retrieving order or items for tracking number {t_no}: {e}")
        context = {'error_message': 'An error occurred while retrieving your order. Please try again later.'}

    return render(request, 'views.html', context)

def already(request):
    return render(request,'already.html')

def Incorrect(request):
    return render(request,'wrong.html')

def Password(request):
    return render(request,'Password.html')

def Send(request):
    return render(request,'Send Message.html')

def Feed(request):
    return render(request,'Feed.html')

def Pay(request):
    return render(request,'Pay.html')



@login_required
def payment_success(request):
    # Save order details and clear the cart
    cartitems = Cart.objects.filter(user=request.user)
    if cartitems:
        order = Order.objects.create(
            user=request.user,
            total_price=sum(item.product.Selling_Price * item.product_qty for item in cartitems),
        )
        for item in cartitems:
            order.items.add(item)  # Assuming a Many-to-Many field in the Order model
        cartitems.delete()  # Clear the cart

    return redirect('order_history')



############################### Razorpay Views #######################
def Razorpaycheck(request):
    # Calculate total price
    rawcart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in rawcart:
        total_price += item.product.Selling_Price * item.product_qty

    # Return the price to the frontend for Razorpay integration
    return JsonResponse({'total_price': total_price})









@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})


def Gallary(request):
    photos = Photo.objects.filter()  # Renamed variable to avoid conflict
    context = {'photo': photos}  # Keep the key as 'photo' for template consistency
    return render(request, 'Gall.html', context)


def Vidios(request):
    return render(request,'Vidio.html')    


def Companies(request):
    brands = Brands.objects.all()  # Fetch all Brand objects
    context = {'Brands': brands}  # Corrected the key name to lowercase
    return render(request, 'Companies.html', context)  # Pass the context to render


#-------------------------------------- Order Tracker--------------------------------------#
def order_tracker(request, tracking_no):
    # Fetch data from the correct model (OrderTracker)
    order = get_object_or_404(OrderTracker, tracking_no=tracking_no)
    
    # Calculate delivery progress
    if order.delivery_date:  # Ensure delivery_date exists
        total_days = (order.delivery_date - order.order_date).days
        remaining_days = (order.delivery_date - date.today()).days
        progress = max(0, ((total_days - remaining_days) / total_days) * 100)
    else:
        total_days = remaining_days = progress = 0

    context = {
        'order': order,
        'progress': progress,  # Percentage of order completion
        'remaining_days': remaining_days if remaining_days > 0 else 0,
    }
    return render(request, 'Order_tracker.html', context)

def order_view(request, tracking_no):
    order = get_object_or_404(OrderTracker, tracking_no=tracking_no)  # Correct model
    orderitems = order.items.all() if hasattr(order, 'items') else []  # Adjust for your structure
    return render(request, 'template_name.html', {'order': order, 'orderitems': orderitems})


@csrf_exempt
def clear_cart(request):
    if request.method == 'POST':
        # Get payment ID and order status from request
        payment_id = request.POST.get('payment_id')
        order_status = request.POST.get('order_status')

        if order_status == "completed":
            # Mark the order as completed or do any other order-related logic
            user = request.user
            cart_items = Cart.objects.filter(user=user)
            total_price = sum(item.product.Selling_Price * item.quantity for item in cart_items)

            order = Order(user=user, total_price=total_price, payment_id=payment_id, status="Completed")
            order.save()

            # Empty the user's cart after successful payment
            cart_items.delete()

            return JsonResponse({"status": "success", "message": "Order completed and cart cleared."})
        else:
            return JsonResponse({"status": "error", "message": "Payment failed"})
    return JsonResponse({"status": "error", "message": "Invalid request"})


def OrderSuccess(request):
    return render(request, 'order_success.html')



def BLOG(request):
    blogs = Blog.objects.filter()  # Fetch blogs associated with the logged-in user
    context = {'blogs': blogs}  # Pass the blogs to the template
    return render(request, 'blog.html', context)