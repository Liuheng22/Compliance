import json
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

'''测试数据'''
class TestData(models.Model):
    key = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    cid = models.CharField(max_length=100)

'''问题'''
class Problem(models.Model):
    pid = models.IntegerField()
    col = models.CharField(max_length=50)
    seriousness = models.CharField(max_length=50)
    ptype = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    fix = models.CharField(max_length=200)

    def __init__(self,pid_,col_,seriousness_,ptype_,description_,fix_=""):
        self.pid = pid_
        self.col = col_
        self.seriousness = seriousness_
        self.ptype = ptype_
        self.description = description_
        self.fix = fix_

class ProblemEncoder(json.JSONEncoder):
    def default(self,obj):
        # 将类转换成dict
        d = {}
        d['__class__'] = obj.__class__.__name__
        d['__module__'] = obj.__module__
        d.update(obj.__dict__)
        return d

class ProblemDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self,object_hook=self.dict2object)
    def dict2object(self,d):
        # 转化dict为类
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module,class_name)
            args = dict((key.encode('ascii'),value) for key,value in d.items())
            inst = class_(**args)
        else:
            inst = d
        return inst