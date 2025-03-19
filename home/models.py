from django.db import models
from django.db.models import Max, UniqueConstraint
from django.utils.text import slugify

# Brand Model
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="images/", null=True, blank=True)
    isfeatured = models.BooleanField(default=False)
    about = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Category Model (Men, Women, Unisex)
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Product Model (Tshirt, Shirt, Trouser)
class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Color Model
class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hexCode = models.CharField(max_length=7, help_text="Hex code for color")

    def __str__(self):
        return self.name

# Size Model
class Size(models.Model):
    size_label = models.CharField(max_length=10, unique=True)  # e.g., S, M, L, XL

    def __str__(self):
        return self.size_label

# Size Guide Model (Different for each Brand)
class SizeGuide(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    chest = models.FloatField()
    waist = models.FloatField()
    hip = models.FloatField()

    def __str__(self):
        return f"{self.brand.name} - {self.size.size_label}"

# Listing Model (Main Product Listing)
class Listing(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    productType = models.ForeignKey(ProductType, on_delete=models.CASCADE, blank=True, null=True)
    uniqueLabel = models.PositiveIntegerField(blank=True, null=True)
    colors = models.ManyToManyField(Color)
    sizes = models.ManyToManyField(Size)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discountedPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    productDetails = models.TextField(blank=True, null=True)
    deliveryTime = models.CharField(max_length=255, default="5-7 days")
    stockQuantity = models.PositiveIntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    returnEligible = models.BooleanField(default=False)
    exchangeEligible = models.BooleanField(default=False)
    bestSelling = models.BooleanField(default=False)
    newArrival = models.BooleanField(default=False)
    specialOffer = models.BooleanField(default=False)
    

    class Meta:
        constraints = [
            UniqueConstraint(fields=['productType', 'uniqueLabel'], name='unique_product_label')
        ]

    def save(self, *args, **kwargs):
        # Assign uniqueLabel if not already set
        if not self.uniqueLabel and self.productType:
            last_label = Listing.objects.filter(productType=self.productType).aggregate(Max('uniqueLabel'))['uniqueLabel__max']
            self.uniqueLabel = 1 if last_label is None else last_label + 1
        
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


        super().save(*args, **kwargs)


    def final_price(self):
        return self.discountedPrice if self.discountedPrice else self.price

    def __str__(self):
        return f"{self.brand} - {self.name}"

# Image Model (To Store Multiple Images)
class Image(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return f"Image for {self.listing.name}"
