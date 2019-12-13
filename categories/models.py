from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(category_pre_save_receiver, sender=Category)