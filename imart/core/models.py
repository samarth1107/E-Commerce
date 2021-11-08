from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from .scripts import file_size
from django.core.validators import FileExtensionValidator


AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('email').blank = False
AbstractUser._meta.get_field('email').null = False
AbstractUser._meta.get_field('first_name').blank = False
AbstractUser._meta.get_field('first_name').null = False
AbstractUser._meta.get_field('last_name').blank = False
AbstractUser._meta.get_field('last_name').null = False
class profile(AbstractUser):
    #---Address fields---
    address_1 = models.CharField("address line 1", max_length=128, blank=False)
    address_2 = models.CharField("address line 2", max_length=128, blank=True)
    city = models.CharField("city", max_length=64, blank=False)
    state = models.CharField("state", max_length=64, blank=False)
    zip_code = models.IntegerField("zip code", validators=[MinValueValidator(100000), MaxValueValidator(999999)], blank=False, default=100000)
    #---Address fields ends---

    file = models.FileField(upload_to="image/approval", null=True, blank=True,validators=[file_size,FileExtensionValidator(allowed_extensions=['pdf'])])
    is_admin= models.BooleanField('Is admin', default=False)
    is_customer = models.BooleanField('Is customer', default=False)
    is_seller = models.BooleanField('Is seller', default=False)

    verified = models.BooleanField(default=False)
    encrypted_OTP = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.username)

class products(models.Model):
    Product_id = models.AutoField(primary_key=True)
    username=models.ForeignKey(to='profile', on_delete=models.CASCADE)
    Product_image = models.ImageField(upload_to="image/products")
    Product_image_2 = models.ImageField(upload_to="image/products")
    Product_title  = models.CharField(max_length=100)
    Brand = models.CharField(max_length=50)
    Product_mrp  = models.PositiveIntegerField()
    Selling_price = models.PositiveIntegerField()
    category_id  = models.ForeignKey(to='product_category', on_delete=models.CASCADE)
    Product_description  = models.CharField(max_length=600)
    Quantity_available = models.PositiveIntegerField()
    Listing_status = models.PositiveIntegerField()
    Country_of_origin = models.CharField(max_length=100)
    Avg_rating = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

class product_category(models.Model):
    Category_id = models.PositiveIntegerField()

    category_name = [
        ('Capital_Goods', 'Capital Goods'),
        ('Club_Goods', 'Club Goods'),
        ('Commodities', 'Commodities'),
        ('Common_Goods', 'Common Goods'),
        ('Consumer_Durables', 'Consumer Durables'),
        ('Consumer_Goods', 'Consumer Goods'),
        ('Digital_Goods', 'Digital Goods'),
        ('Durable_Goods', 'Durable Goods'),
        ('Economic_Goods', 'Economic Goods'),
        ('Experience_Goods', 'Experience Goods'),
        ('Final_Goods', 'Final Goods'),
        ('FMCG', 'FMCG'),
        ('Inferior_Good', 'Inferior Good'),
        ('Intangible_Goods', 'Intangible Goods'),
        ('Luxury_Goods', 'Luxury Goods'),
        ('Merit_Good', 'Merit Good'),
        ('Search_Good', 'Search Good'),
        ('Soft_Goods', 'Soft Goods'),
        ('Substitute_Good', 'Substitute Good'),
        ('Superior_Goods', 'Superior Goods'),
        ('Unsought_Goods', 'Unsought Goods'),
        ('Veblen_Goods', 'Veblen Goods')
    ]

    Name = models.CharField(
        max_length=20,
        choices=category_name,
        default='Consumer_Goods',
    )

    Description = models.CharField(max_length=600)

    class Meta:
        verbose_name = 'product category'
        verbose_name_plural = 'product categories'
    
    def __str__(self):
        return self.Name

class Cart(models.Model):
    user = models.ForeignKey(to=profile, on_delete=models.CASCADE)
    product = models.ForeignKey(to=products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'