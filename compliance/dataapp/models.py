from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.

'''用户表'''
class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['c_time']


'''任务表'''
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    body = models.TextField()
    upload = models.FileField(upload_to='files/')

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


    objects = models.Manager()  # The default manager.
    # published = PublishedManager()  # Our custom manager.

    def get_absolute_url(self):
        return reverse('dataapp:post_detail', args=[self.slug])


'''操作表'''
class Operation(models.Model):
    content = models.CharField(max_length=500)
    task = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_operation')
    quantity = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)
      

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.content
