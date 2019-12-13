from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.db.models.signals import pre_save
from categories.models import Category
from django.urls import reverse


def product_directory_path(instance, filename):
    return 'product_{0}/{1}'.format(instance.title, filename)


class ProductSizes(models.Model):
    size = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Product Sizes"

    def __str__(self):
        return self.size


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to=product_directory_path)
    slug = models.SlugField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category)
    sizes = models.ManyToManyField(ProductSizes)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product", kwargs={'slug': self.slug})

    def add_to_cart(self):
        return reverse("cart:add-to-cart", kwargs={'slug': self.slug})

    def remove_from_cart(self):
        return reverse("cart:remove-from-cart", kwargs={'slug': self.slug})
    
    def remove_single_from_cart(self):
        return reverse("cart:remove-single-item-from-cart", kwargs={'slug': self.slug})

    def amount_saved(self):
        return self.price - self.discount_price

    def get_descount_prec(self):
        return self.price - (self.price * self.discount_price / 100)

    def get_final_price(self):
        if self.discount_price:
            return self.price - self.discount_price
        return self.price


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(product_pre_save_receiver, sender=Product)