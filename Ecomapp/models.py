from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import timedelta, date
import os


def get_file_path(instance, filename):
    original_filename = filename
    now_time = datetime.datetime.now().strftime('%y%m%d%H%M%S')
    filename ="%s%s" %(now_time,original_filename)
    return os.path.join('uploads/', filename)
    return f"uploads/videos/{filename}"
    return f"uploads/brands/{filename}"

class Category(models.Model):  
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="Whether the category is hidden or not")
    trending = models.BooleanField(default=False, help_text="Whether the category is trending or not")
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.TextField(null=False, blank=False)
    meta_description = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Photo(models.Model):  
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Brands(models.Model):  
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Logo(models.Model):  
    Logo = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    Description = models.CharField(max_length=1200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Video(models.Model):
    title = models.CharField(max_length=255)  # Title of the video
    description = models.TextField(blank=True, null=True)  # Description of the video
    video_file = models.FileField(upload_to=get_file_path)  # Video file upload
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time the video was created

   


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    Product_image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    Small_description = models.TextField(max_length=250, null=False, blank=False)
    Size = models.TextField(max_length=150,null=True,blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    description = models.TextField(max_length=1000, null=False, blank=False)
    description2 = models.TextField(max_length=1000, null=True, blank=False)
    Orignal_Price = models.FloatField(null=False, blank=False)
    Selling_Price =models.FloatField(null=False,blank=False)
    status = models.BooleanField(default=False, help_text="Whether the category is hidden or not")
    trending = models.BooleanField(default=False, help_text="Whether the category is trending or not")
    Tag = models.CharField(max_length=150, null=False, blank=False)
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.TextField(null=False, blank=False)
    meta_description = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    product_qty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    
class Newproducts(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    Product_image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    Small_description = models.TextField(max_length=250, null=False, blank=False)
    Quantity = models.IntegerField(null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    Orignal_Price = models.FloatField(null=False, blank=False)
    Selling_Price =models.FloatField(null=False,blank=False)
    status = models.BooleanField(default=False, help_text="Whether the category is hidden or not")
    trending = models.BooleanField(default=False, help_text="Whether the category is trending or not")
    Tag = models.CharField(max_length=150, null=False, blank=False)
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.TextField(null=False, blank=False)
    meta_description = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE ,related_name="Product")    
    image = models.ImageField(upload_to="product")    


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)





class Category1(models.Model):  
    slug = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to='path/to/upload', null=True, blank=True)
    name = models.CharField(max_length=150, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="Whether the category is hidden or not")
    trending = models.BooleanField(default=False, help_text="Whether the category is trending or not")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class subCategory(models.Model):
    category = models.ForeignKey(Category1, on_delete=models.CASCADE, null=True)  # Temporarily allow null
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to='path/to/upload', null=True, blank=True)
    small_description = models.TextField(max_length=250, null=True, blank=False)
    quantity = models.IntegerField(null=True, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=False)
    original_price = models.FloatField(null=True, blank=False)
    selling_price = models.FloatField(null=True, blank=False)  
    status = models.BooleanField(default=False, help_text="Whether the category is hidden or not")
    trending = models.BooleanField(default=False, help_text="Whether the category is trending or not")
    tag = models.CharField(max_length=150, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Arrival(models.Model):  
    slug = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to='path/to/upload', null=True, blank=True)
    name = models.CharField(max_length=150, null=False, blank=False)
    MRP =  models.FloatField(max_length=150,null=True, blank=False)
    SP  =  models.FloatField(max_length=150,null=True,blank=False)
    status = models.BooleanField(default=False, help_text="Whether the category is hidden or not")
    trending = models.BooleanField(default=False, help_text="Whether the category is trending or not")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Demand(models.Model):  
    slug = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to='path/to/upload', null=True, blank=True)
    name = models.CharField(max_length=150, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="Whether the category is hidden or not")
    MRP  =  models.FloatField(null=True,blank=False)    
    SP   =  models.FloatField(null=True,blank=True)
    trending = models.BooleanField(default=False, help_text="Whether the category is trending or not")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Delership(models.Model):
     image = models.ImageField(upload_to='path/to/upload', null=True, blank=True)




class Contact(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField()
    Phone = models.CharField(max_length=200)
    Message = models.TextField()
    
    def __str__(self):
        return self.Name
    

class Feedback(models.Model):
    Name2 = models.CharField(max_length=200)
    Email2 = models.EmailField()
    Phone2 = models.CharField(max_length=200)
    Product2 = models.CharField(max_length=200)
    Message2 = models.TextField()



class Complaint(models.Model):
    Name3 = models.CharField(max_length=200)
    Email3 = models.EmailField()
    Phone3 = models.CharField(max_length=200)
    Product3 = models.CharField(max_length=200)
    Model3 = models.CharField(max_length=200)
    Uploadbill3 = models.ImageField(upload_to=get_file_path, null=True, blank=True)   
    Message3 = models.TextField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Fname = models.CharField(max_length=100)
    Lname = models.CharField(max_length=100)
    Email = models.EmailField()
    Phone = models.CharField(max_length=15)
    Address = models.TextField()
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Country = models.CharField(max_length=100)
    Pincode = models.CharField(max_length=10)
    Payment_mode = models.CharField(max_length=20)  # COD or Razorpay
    Payment_id = models.CharField(max_length=100, null=True, blank=True)  # Razorpay payment ID
    Total_price = models.FloatField()
    tracking_no = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.tracking_no} by {self.user.username}"    

class Orderitem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    Product =models.ForeignKey(Product,on_delete = models.CASCADE)
    Price = models.FloatField(null=False,default=False)
    Quantity =models.IntegerField(null=False, default=False)
   

    def __str__(self):
         return'{} {}' .format (self.order.id,self.order.tracking_no)
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE) 
    phone= models.CharField(max_length=50,null=False)
    address= models.CharField(max_length=50,null=False)
    city= models.CharField(max_length=50,null=False)
    state= models.CharField(max_length=50,null=False)
    country= models.CharField(max_length=50,null=False)
    pincode= models.CharField(max_length=50,null=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    




class Orderhistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Cart')  # Adjust based on your cart model
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


# order View Tracker #
class OrderTracker(models.Model):
    Fname = models.CharField(max_length=100)
    Lname = models.CharField(max_length=100)
    Email = models.EmailField()
    Phone = models.CharField(max_length=15)
    Address = models.TextField()
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Country = models.CharField(max_length=100)
    Pincode = models.CharField(max_length=10)
    Total_price = models.DecimalField(max_digits=10, decimal_places=2)
    Status = models.CharField(max_length=50, default='Pending')  # Pending, Shipped, Delivered
    tracking_no = models.CharField(max_length=50, unique=True)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(blank=True, null=True)

def save(self, *args, **kwargs):
        # Automatically set delivery date to 10-15 days after order_date
        if not self.delivery_date:
            self.delivery_date = self.order_date + timedelta(days=10)
        super().save(*args, **kwargs)    

class Blog(models.Model):  # Class name should be in PascalCase
    product_image = models.ImageField(upload_to='uploads/blog_images/', null=True, blank=True)        
    heading = models.CharField(max_length=150, null=False, blank=False)  # CharField for headings is generally sufficient
    description = models.TextField(max_length=1800, null=False, blank=False)  # Fixed typo 'max_legth'

    