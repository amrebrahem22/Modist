from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


User = settings.AUTH_USER_MODEL

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    content = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta: 
        ordering = ['-timestamp']

    # will return all replies
    def children(self): #replies
        return Comment.objects.filter(parent=self)
    
