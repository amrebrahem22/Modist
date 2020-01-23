from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from .models import Post, PostCategory
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from taggit.models import Tag
from django.db.models import Q

class BlogListView(ListView):
    queryset = Post.objects.all()
    template_name = 'blog.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        qs = self.request.GET.get('q')
        queryset = super(BlogListView, self).get_queryset()
        if qs:
            queryset = queryset.filter(
                Q(title__icontains=qs) |
                Q(content__icontains=qs) |
                Q(overview__icontains=qs) |
                Q(author__username__icontains=qs) |
                Q(tags__name__icontains=qs) |
                Q(category__name__icontains=qs)
            ).distinct()
        return queryset


def blog_post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        message = request.POST.get('message')
        parent = request.POST.get('parent')
        message_reply = request.POST.get('message_reply')

        comment_parent = None
        qs_parent = Comment.objects.filter(id=parent)
        if qs_parent.exists():
            comment_parent = qs_parent.first()

        if request.user.is_authenticated:
            if parent and message_reply and not message:
                comment_reply = Comment.objects.create(
                user = request.user,
                content_object=post,
                object_id = post.id,
                content = message_reply,
                parent=comment_parent
                )
            else:
                comment_obj = Comment.objects.create(
                    user = request.user,
                    content_object=post,
                    object_id = post.id,
                    content = message,
                )
            return redirect(post.get_absolute_url())
            
    comments = Comment.objects.filter(object_id=post.id, parent=None)
    # tags = None
    # if post.tags:
    #     tags = post.tags.split(', ')
    cats = PostCategory.objects.all()[:6]
    common_tags = Post.tags.most_common()[:9]
    recent_posts = Post.objects.all().order_by('-timestamp')[:3]
    context = {'post': post, 'comments': comments, 'common_tags':common_tags, 'cats': cats, 'recent_posts': recent_posts}
    return render(request, 'blog-single.html', context)
