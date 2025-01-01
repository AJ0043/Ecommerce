from django.views.generic import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Ensure you have a valid view called 'home'
    path('collections', views.collections, name='collections'),
    path("collections/<str:slug>",views.collectionsview,name="collectionsview"),
    path("collections/<str:cate_slug>/<str:prod_slug>",views.productview,name="productview"),
    path('features/', views.feature, name='Features'),  # Ensure you have a valid view called 'home'
    path('About/', views.Aboutus, name='Aboutus'),
    path('Contact/', views.Contactus, name='Contact'),
    path('Feedback/', views.FeedbackView, name='Feedbacks'),
    path('Complaint1/', views.Complaint, name='Complaint'),
    path('Login/', views.Login, name='Login'),
    path('Signup/', views.Signup, name='Signup'),
    
    
    path('Cart/', views.cart, name='Cart'),
    path('add-to-cart/', views.Cart2, name='addtocart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('delete-cart-item/', views.delete_cart_item, name='delete_cart_item'),
    path('placeOrder/', views.placeorder2, name='placeorder'),
    path('Pay/', views.Pay, name='Pay'),
    path('Gall/',views.Gallary,name='Gallery'),
    path('Vidios/',views.Vidios,name='Vidios'),
    path('blog/', views.BLOG, name='blog_detail'),
    path('Wishlist/', views.Wishlists, name='Wishlist'),
    path('add-to-Wishlist/', views.addWishlist, name='addtoWishlist'),
    path('delete-list-item/', views.delete_list_item, name='delete_list_item'),
    path('product-list/', views.productlist, name='product-list'),
    path('search-product/', views.searchproduct, name='searchproduct'),
    path('search-results/', views.search_results, name='search_results'),
    path('Companies/', views.Companies, name='Companies'),
    
    

    # all urls releted a Messages.....
    path('Checkout/', views.Check, name='Checkout'),
    path('Booking/', views.Book, name='Booking'),
    path('Logout3/',views.Logout, name="logout"),
    path('already/', views.already, name='log'),
    path('Incorrect/',views.Incorrect, name="wrong"),
    path('NotResponse/',views.Password, name="notmatch"),
    path('SendMessage/', views.Send, name='success'),
    path('Feed/', views.Feed, name='Feedback'),
    path('order-view/<str:t_no>/', views.vieworder, name='vieworder'),
    




# Email Integration Urls ###
   path('activate/<uidb64>/<token>/', views.activate, name='activate'),



#Dashborad Url ##
path('Dashboard/' , views.Dash ,name='Dashboard'),
path('Customer/' , views.Customer ,name='Customer'),
path('orders/', views.order_list, name='order_list'),
path('contact-list/', views.contact_list_view, name='contact_list'),
path('feedback3/', views. Feedback2, name='feedback_list'),
path('complent/',views. complaint_list, name='complaint_list'),


############ Razorpay Url ######
path('proceed-to-pay/', views.Razorpaycheck, name='Payment'),
path('order-history/', views.order_history, name='order_history'),
path('order/tracker/<str:tracking_no>/', views.order_tracker, name='order_tracker'),
path('clear_cart/', views.clear_cart, name='clear_cart'),
path('order-success/', views.OrderSuccess, name='OrderSuccess'),


]









