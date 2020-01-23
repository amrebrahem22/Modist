from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.urls import reverse
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from taggit.managers import TaggableManager
from django.template.defaultfilters import stringfilter
import markdown as md

User = settings.AUTH_USER_MODEL

class PostCategory(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(null=True, blank=True, max_length=200,
                            db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def category_posts_count(self):
        return self.post_category.all().count()


    def __str__(self):
        return self.name

def post_save_category_slug(sender, instance, created, *args, **kwargs):
    if created and instance.slug is None and instance.name:
        instance.slug = slugify(instance.name)
                    
        instance.save()

post_save.connect(post_save_category_slug, sender=PostCategory)


class Post(models.Model):
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(null=True, blank=True)
    overview    = models.CharField(max_length=250)
    content     = models.TextField()
    author      = models.ForeignKey(User, on_delete=models.CASCADE)
    tags        = TaggableManager()
    category    = models.ManyToManyField(PostCategory, related_name='post_category')
    image       = models.ImageField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp']

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        # return mark_safe(markdown_text)
        return md.markdown(content, extensions=['markdown.extensions.fenced_code'])

    def get_overview(self):
        content = self.overview
        markdown_text = markdown(content)
        # return mark_safe(content)
        return md.markdown(content, extensions=['markdown.extensions.fenced_code'])


def post_save_post_title(sender, instance, created, *args, **kwargs):
    if created and instance.slug is None and instance.title:
        instance.slug = slugify(instance.title)
                    
        instance.save()

post_save.connect(post_save_post_title, sender=Post)
