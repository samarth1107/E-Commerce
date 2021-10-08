from django.db import models

# Create your models here.
class products(models.Model):
    Product_id = models.PositiveIntegerField(primary_key=True)
    Seller_id = models.PositiveIntegerField()
    Product_image = models.ImageField(upload_to="products")
    Product_title  = models.CharField(max_length=100)
    Brand = models.CharField(max_length=50)
    Product_mrp  = models.PositiveIntegerField()
    Selling_price = models.PositiveIntegerField()
    category_id  = models.PositiveIntegerField()
    Sub_category_1 = models.
    Sub_category_2 = models.
    Sub_category_3 = models.
    Sub_category_4 = models.
    Product_description  = models.
    Bullet_points = models.
    Manufacturer = models.
    Quantity_available = models.
    Pack_of = models.
    Colour = models.
    Item_weight = models.
    Listing_status = models.
    Country_of_origin = models.
    Hsn = models.
    Tax_percent = models.PositiveIntegerField()
    Avg_rating = models.PositiveIntegerField()
